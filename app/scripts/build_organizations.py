import json
import re
from pathlib import Path

from app.services.database_service import DatabaseService


def normalize(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    return name


def split_name(name: str):
    """
    Returns:
        canonical_name
        abbreviation
    """

    name = normalize(name)

    match = re.search(r"\((.*?)\)", name)

    if match:

        abbr = match.group(1).strip()

        canonical = re.sub(
            r"\s*\(.*?\)",
            "",
            name
        ).strip()

        return canonical, abbr

    return name, None


organizations = {}

with DatabaseService() as db:

    rows = db.get_distinct_organizations()

    for org in rows:

        canonical, abbr = split_name(org)

        key = canonical.lower()

        organizations.setdefault(key, set())

        organizations[key].add(org.lower())
        organizations[key].add(canonical.lower())

        if abbr:
            organizations[key].add(abbr.lower())

        # automatic aliases
        short = canonical.lower()

        short = short.replace("ministry of ", "")
        short = short.replace("authority", "")
        short = short.replace("department", "")
        short = short.replace("corporation", "")

        short = re.sub(r"\s+", " ", short).strip()

        if short:
            organizations[key].add(short)

# merge manual aliases
alias_file = Path("app/data/organization_aliases.json")

if alias_file.exists():

    with open(alias_file, encoding="utf8") as f:

        extra = json.load(f)

    for key, aliases in extra.items():

        organizations.setdefault(key.lower(), set())

        organizations[key.lower()].update(
            map(str.lower, aliases)
        )

# convert set -> list
organizations = {
    k: sorted(v)
    for k, v in organizations.items()
}

with open(
    "app/data/organizations.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        organizations,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"Generated {len(organizations)} organizations.")