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
            "cctv",
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
            "Generator",
        }
        self.PAK_CITIES = [
            "karachi",
            "lahore",
            "islamabad",
            "rawalpindi",
            "peshawar",
            "quetta",
            "multan",
            "faisalabad",
            "hyderabad",
            "sialkot",
            "gujranwala",
            "sukkur",
        ]
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

    def filter_tenders(self, results,question):
        filtered = []
        current_time = datetime.now()
        question_lower = question.lower()
        location = None
        for city in self.PAK_CITIES:
            if re.search(r"\b"+re.escape(city)+r"\b",question_lower):
                location = city
                break
    

        for result in results:
          
            title = str(result.get("title", "")).lower()
            org = str(result.get("organization", "")).lower()
            dept = str(result.get("department", "")).lower()
            cat = str(result.get("category", "")).lower()
            loc = str(result.get("location", "")).lower()
            text = str(result.get("text", "")).lower()

            if location:
                if location not in loc:
                    continue
            full_searchable = f"{title} {org} {dept} {cat} {loc} {text}"

           
            tech_matches = 0
            for kw in self.ALL_TECH_KEYWORDS:
                
                if re.search(r"\b" + re.escape(kw) + r"\b", full_searchable):
                   
                    if re.search(
                        r"\b" + re.escape(kw) + r"\b", title
                    ) or re.search(r"\b" + re.escape(kw) + r"\b", cat):
                        tech_matches += 3
                    else:
                        tech_matches += 1

          
            if tech_matches == 0:
                continue

           
            trap_score = sum(
                2
                for trap in self.PHYSICAL_TRAPS
                if re.search(r"\b" + re.escape(trap) + r"\b", full_searchable)
            )

            
            final_relevance_score = tech_matches - trap_score

            
            if final_relevance_score <= 0:
                continue

            result["final_relevance_score"] = max(0, final_relevance_score)
            
            filtered.append(result)


        filtered.sort(
            key=lambda x: (
               
                x["final_relevance_score"],  # Highest custom match score
                x.get("score", 0),  # Baseline vector rank
            ),
            reverse=True,
        )

        return filtered