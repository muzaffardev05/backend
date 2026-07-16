import json
import re
from pathlib import Path


class OrganizationParser:

    def __init__(self):

        file_path = (
            Path(__file__)
            .parent.parent
            / "data"
            / "organizations.json"
        )
        
        with open(file_path, "r", encoding="utf-8") as f:
            self.organizations = json.load(f)
            

    def extract(self, text: str):

        remaining = text
        found = []

        lower = text.lower()

        for canonical, aliases in self.organizations.items():

            for alias in aliases:

                pattern = r"\b{}\b".format(
                    re.escape(alias.lower())
                )

                if re.search(pattern, lower):

                    if canonical not in found:
                        found.append(canonical)

                    remaining = re.sub(
                        pattern,
                        "",
                        remaining,
                        flags=re.IGNORECASE,
                    )

                    break

        remaining = re.sub(
            r"\s+",
            " ",
            remaining
        ).strip()

        return found, remaining
    



# parser = OrganizationParser()

# organizations, remaining = parser.extract(
#     "IT security tenders from ksew in Karachi"
# )

# print(organizations)
# print(remaining)