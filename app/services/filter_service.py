from datetime import datetime
import re


class FilterService:

    def __init__(self):
        # Define core domain watchlists
        self.IT_KEYWORDS = {
            "server",
            "switch",
            "router",
            "ups",
            "datacenter",
            "storage",
            "nas",
            "san",
            "cloud",
            "fiber",
            "lan",
            "wan",
            "bras",
            "computing",
        }

        self.SECURITY_KEYWORDS = {
            "firewall",
            "ngfw",
            "ids",
            "ips",
            "cyber",
            "soc",
            "encryption",
            "siem",
            "antivirus",
            "threat",
            "penetration",
            "scada",
            "network security",
        }

        self.COMMUNICATIONS_KEYWORDS = {
            "antenna",
            "amplifier",
            "rf module",
            "microwave",
            "telecom",
            "voice",
            "transceiver",
            "radio",
            "telecommunication",
            "vccs",
            "satellite",
            "frequency",
        }

        # Merge all into a master tech set
        self.ALL_TECH_KEYWORDS = self.IT_KEYWORDS.union(
            self.SECURITY_KEYWORDS, self.COMMUNICATIONS_KEYWORDS
        )

        # Aggressive physical & civil works traps to clean your RAG noise
        self.PHYSICAL_TRAPS = {
            "wall",
            "posts",
            "paint",
            "civil",
            "cement",
            "bricks",
            "guard",
            "cctv",
            "barbed",
            "furniture",
            "chair",
            "stationery",
            "toner",
            "paper",
            "janitorial",
            "catering",
            "renovation",
            "gate",
        }

    def filter_tenders(self, results, question):
        filtered = []
        current_time = datetime.now()

        for result in results:
            # 1. Build structured searchable blocks
            title = str(result.get("title", "")).lower()
            org = str(result.get("organization", "")).lower()
            dept = str(result.get("department", "")).lower()
            cat = str(result.get("category", "")).lower()
            loc = str(result.get("location", "")).lower()
            text = str(result.get("text", "")).lower()

            # Flatten text fields for regex scanning
            full_searchable = f"{title} {org} {dept} {cat} {loc} {text}"

            # 2. Domain Keyword Processing (Looking for whole-word matches)
            tech_matches = 0
            for kw in self.ALL_TECH_KEYWORDS:
                # \b ensures exact word/phrase boundary matching
                if re.search(r"\b" + re.escape(kw) + r"\b", full_searchable):
                    # Give higher weight if the tech keyword appears in the Title or Category
                    if re.search(
                        r"\b" + re.escape(kw) + r"\b", title
                    ) or re.search(r"\b" + re.escape(kw) + r"\b", cat):
                        tech_matches += 3
                    else:
                        tech_matches += 1

            # 3. Filter Gate: If it doesn't match your domain tech keywords, skip it entirely
            if tech_matches == 0:
                continue

            # 4. Trap Detection: Penalize or drop physical/civil works masquerading as tech security
            trap_score = sum(
                2
                for trap in self.PHYSICAL_TRAPS
                if re.search(r"\b" + re.escape(trap) + r"\b", full_searchable)
            )

            # Adjust score calculation
            final_relevance_score = tech_matches - trap_score

            # If traps heavily outweigh tech terms, drop this tender entirely
            if final_relevance_score <= 0:
                continue

            # 5. Strict Date Validation for Active Status
            is_expired = False
            closing_date_raw = result.get("closing_date") or result.get(
                "Closing Date"
            )

            if closing_date_raw:
                try:
                    # Clean timestamps out of common PPRA variations (e.g. 'Jul 13, 2026 10:45 AM')
                    clean_date = re.sub(
                        r"\s+\d+:\d+.*", "", str(closing_date_raw)
                    ).strip()
                    formats = ["%Y-%m-%d", "%b %d, %Y"]

                    for fmt in formats:
                        try:
                            closing_date = datetime.strptime(clean_date, fmt)
                            if closing_date.date() < current_time.date():
                                is_expired = True
                            break
                        except ValueError:
                            continue
                except Exception:
                    pass

            # Update item attributes for sorting matrix
            result["final_relevance_score"] = max(0, final_relevance_score)
            result["is_expired"] = is_expired

            filtered.append(result)

        # 6. Multi-Tier Ranking Strategy:
        # Tier 1: Active Tenders come before expired ones
        # Tier 2: Highest computed relevance score (Tech Weights - Traps)
        # Tier 3: Underlying Vector Similarity Score from your DB as the ultimate tiebreaker
        filtered.sort(
            key=lambda x: (
                0 if x["is_expired"] else 1,  # Active (1) beats Expired (0)
                x["final_relevance_score"],  # Highest custom match score
                x.get("score", 0),  # Baseline vector rank
            ),
            reverse=True,
        )

        return filtered