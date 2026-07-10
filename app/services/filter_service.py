from datetime import datetime
import re


class FilterService:

    def __init__(self):

        # -----------------------------
        # Technical keywords
        # -----------------------------
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

        self.COMMUNICATION_KEYWORDS = {
            "antenna",
            "amplifier",
            "rf module",
            "microwave",
            "telecom",
            "telecommunication",
            "voice",
            "radio",
            "transceiver",
            "satellite",
            "frequency",
            "generator",
            "vccs",
        }

        self.ALL_TECH_KEYWORDS = (
            self.IT_KEYWORDS
            | self.SECURITY_KEYWORDS
            | self.COMMUNICATION_KEYWORDS
        )

        # -----------------------------
        # Noise / Physical keywords
        # -----------------------------
        self.PHYSICAL_TRAPS = {
            "wall",
            "paint",
            "cement",
            "brick",
            "bricks",
            "steel",
            "pipe",
            "road",
            "bridge",
            "building",
            "construction",
            "civil",
            "furniture",
            "chair",
            "table",
            "paper",
            "stationery",
            "toner",
            "catering",
            "janitorial",
            "gate",
            "guard",
            "barbed",
            "renovation",
        }

    # ======================================================
    # Helper Methods
    # ======================================================

    def _normalize(self, value):
        """
        Convert None -> ""
        Strip spaces
        Lowercase
        """

        if value is None:
            return ""

        return str(value).strip().lower()

    # ------------------------------------------------------

    def _parse_date(self, value):
        """
        Converts database values to date.

        Supports

        datetime
        YYYY-MM-DD
        YYYY-MM-DD HH:MM:SS
        """

        if not value:
            return None

        if isinstance(value, datetime):
            return value.date()

        if hasattr(value, "date"):
            return value.date()

        value = str(value)

        formats = (
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
        )

        for fmt in formats:

            try:

                return datetime.strptime(
                    value,
                    fmt
                ).date()

            except ValueError:

                pass

        return None

    # ------------------------------------------------------

    def _build_searchable_text(self, result):

        fields = [

            result.get("title", ""),

            result.get("organization", ""),

            result.get("department", ""),

            result.get("category", ""),

            result.get("location", ""),

            result.get("text", ""),

        ]

        return " ".join(
            self._normalize(f)
            for f in fields
        )

    # ------------------------------------------------------

    def _matches_location(
        self,
        result_location,
        filters,
    ):

        locations = filters.get("location", [])

        if not locations:
            return True

        result_location = self._normalize(
            result_location
        )

        return any(
            location in result_location
            for location in locations
        )

    # ------------------------------------------------------

    def _matches_organization(
        self,
        result_org,
        filters,
    ):

        organizations = filters.get(
            "organization",
            [],
        )

        if not organizations:
            return True

        result_org = self._normalize(
            result_org
        )

        return any(
            org in result_org
            for org in organizations
        )

    # ------------------------------------------------------

    def _matches_status(
        self,
        result_status,
        filters,
    ):

        statuses = filters.get(
            "status",
            [],
        )

        if not statuses:
            return True

        return result_status in statuses

    # ------------------------------------------------------

    def _matches_publish_date(
        self,
        publish_date,
        filters,
    ):

        date_filter = filters.get(
            "publish_date"
        )

        if not date_filter:
            return True

        publish_date = self._parse_date(
            publish_date
        )

        if publish_date is None:
            return False

        return (
            date_filter["from"]
            <= publish_date
            <= date_filter["to"]
        )

    # ------------------------------------------------------

    def _matches_closing_date(
        self,
        closing_date,
        filters,
    ):

        date_filter = filters.get(
            "closing_date"
        )

        if not date_filter:
            return True

        closing_date = self._parse_date(
            closing_date
        )

        if closing_date is None:
            return False

        return (
            date_filter["from"]
            <= closing_date
            <= date_filter["to"]
        )

    # ------------------------------------------------------

    def _matches_expired(
        self,
        closing_date,
        filters,
    ):

        expired = filters.get(
            "expired"
        )

        if expired is None:
            return True

        closing_date = self._parse_date(
            closing_date
        )

        if closing_date is None:
            return False

        is_expired = (
            closing_date
            < datetime.now().date()
        )

        return is_expired == expired

    # ------------------------------------------------------

    def _calculate_keyword_score(
        self,
        title,
        category,
        searchable,
        parsed_query
    ):

        score = 0
        keywords=parsed_query["semantic_query"].split()
        

        title = self._normalize(title)
        category = self._normalize(category)

        for keyword in keywords:

            pattern = rf"\b{re.escape(keyword)}\b"

            if not re.search(
                pattern,
                searchable,
            ):
                continue

            if (
                re.search(pattern, title)
                or re.search(pattern, category)
            ):

                score += 3

            else:

                score += 1

        return score

    # ------------------------------------------------------

    def _calculate_trap_score(
        self,
        searchable,
    ):

        score = 0

        for trap in self.PHYSICAL_TRAPS:

            pattern = rf"\b{re.escape(trap)}\b"

            if re.search(
                pattern,
                searchable,
            ):

                score += 2

        return score

    # ------------------------------------------------------

    def _calculate_final_score(
        self,
        result,
        parsed_query
    ):

        searchable = self._build_searchable_text(
            result
        )

        keyword_score = self._calculate_keyword_score(

            result.get("title"),

            result.get("category"),

            searchable,
            parsed_query

        )

        if keyword_score == 0:
            return None

        trap_score = self._calculate_trap_score(
            searchable
        )

        final_score = keyword_score - trap_score

        if final_score <= 0:
            return None

        result["keyword_score"] = keyword_score
        result["trap_score"] = trap_score
        result["final_relevance_score"] = final_score

        return final_score
    # ======================================================
    # Main Filtering Pipeline
    # ======================================================

    def filter_tenders(
        self,
        results,
        parsed_query,
    ):

        filters = parsed_query.get(
            "filters",
            {}
        )

        filtered = []
        

        for result in results:

            # -----------------------------
            # Structured Filters
            # -----------------------------

            if not self._matches_location(
                result.get("location"),
                filters,
            ):
                continue

            if not self._matches_organization(
                result.get("organization"),
                filters,
            ):
                continue

            if not self._matches_status(
                result.get("status"),
                filters,
            ):
                continue

            if not self._matches_publish_date(
                result.get("publish_date"),
                filters,
            ):
                continue

            if not self._matches_closing_date(
                result.get("closing_date"),
                filters,
            ):
                continue

            if not self._matches_expired(
                result.get("closing_date"),
                filters,
            ):
                continue

            # -----------------------------
            # Keyword Scoring
            # -----------------------------

            score = self._calculate_final_score(
                result,
                parsed_query
            )

            if score is None:
                continue

            filtered.append(result)

        # -----------------------------
        # Final Ranking
        # -----------------------------
        
        filtered.sort(
            key=lambda x: (

                # Custom keyword relevance
                x.get(
                    "final_relevance_score",
                    0
                ),

                # Cross Encoder score
                x.get(
                    "rerank_score",
                    0
                ),

                # FAISS similarity
                x.get(
                    "score",
                    0
                ),

                # Latest tenders first
                self._parse_date(
                    x.get(
                        "publish_date"
                    )
                ) or datetime.min.date(),

            ),
            reverse=True,
        )

        return filtered    