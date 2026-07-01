from bs4 import Tag

class PPRAParser:
    """
    Parse a PPRA table row into a standard dictionary.
    """

    def parse(self, row: Tag):

        cols = row.find_all("td")
        
        if len(cols) < 8:
            return None



        tender_no = cols[1].get_text(strip=True)



        detail_items = list(cols[2].stripped_strings)

        title = None
        category = None
        reference_number = None
        organization = None

        if len(detail_items) >= 1:
            title = cols[2].select_one("strong").get_text(strip=True)

        if len(detail_items) >= 2:
            badge_div = cols[2].select_one(
    "div.d-flex.gap-2.flex-wrap.mt-2"
)
            badges = badge_div.select("small")
            category = badges[0].get_text(strip=True)
            reference_number=badges[1].get_text(strip=True)



        if len(detail_items) >= 4:
            organization = detail_items[3]



        org_items = list(cols[3].stripped_strings)
        

        organization_name = None
        department = None
        location = None

        if len(org_items) >= 1:
            organization_name = org_items[0]

        if len(org_items) >= 2:
            department = org_items[1]

        if len(org_items) >= 3:
            location = org_items[2]


        status = cols[4].get_text(strip=True)



        publish_date = cols[5].get_text(strip=True)



        closing_date = cols[6].get_text(" ", strip=True)



        source_url = None

        link = cols[7].find("a")

        if link:

            href = link.get("href")

            if href:

                if href.startswith("http"):
                    source_url = href
                else:
                    source_url = "https://ppra.org.pk" + href



        tender = {

            "tender_no": tender_no,
            "reference_number": reference_number,
            "title": title,
            "website":"PPRA",

            "category": category,

            "organization": organization_name or organization,

            "department": department,

            "location": location,

            "status": status,

            "publish_date": publish_date,

            "closing_date":closing_date,

            "source_url": source_url,

            "documents": []

        }

        return tender