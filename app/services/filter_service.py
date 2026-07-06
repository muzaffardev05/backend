import re


class FilterService:

    def filter_tenders(self, results, question):

        keywords = [
            word
            for word in re.findall(r"\w+", question.lower())
            if len(word) > 2
        ]

        filtered = []

        for result in results:

            searchable = " ".join([
                result.get("title", ""),
                result.get("organization", ""),
                result.get("department", ""),
                result.get("category", ""),
                result.get("location", ""),
                result.get("text", "")
            ]).lower()

            matches = sum(
                keyword in searchable
                for keyword in keywords
            )

            if matches > 0:

                result["keyword_matches"] = matches
                filtered.append(result)

        filtered.sort(
            key=lambda x: (
                x["keyword_matches"],
                x["score"]
            ),
            reverse=True
        )

        return filtered