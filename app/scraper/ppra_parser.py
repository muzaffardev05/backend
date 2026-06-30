from bs4 import Tag


class PPRAParser:
    """
    Parse a PPRA table row into a standard dictionary.
    """

    def parse(self, row: Tag):

        cols = row.find_all("td")

        if len(cols) < 8:
            return None

        # -------------------------------------
        # Tender Number
        # -------------------------------------

        tender_no = cols[1].get_text(strip=True)

        # -------------------------------------
        # Tender Details
        # -------------------------------------

        detail_items = list(cols[2].stripped_strings)

        title = None
        category = None
        # tender_no = None
        organization = None

        if len(detail_items) >= 1:
            title = detail_items[0]

        if len(detail_items) >= 2:
            category = detail_items[1]

        # if len(detail_items) >= 3:
        #     tender_no = detail_items[2]

        if len(detail_items) >= 4:
            organization = detail_items[3]

        # -------------------------------------
        # Organization Details
        # -------------------------------------

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

        # -------------------------------------
        # Status
        # -------------------------------------

        status = cols[4].get_text(strip=True)

        # -------------------------------------
        # Publish Date
        # -------------------------------------

        publish_date = cols[5].get_text(strip=True)

        # -------------------------------------
        # Closing Date
        # -------------------------------------

        closing_date = cols[6].get_text(" ", strip=True)

        # -------------------------------------
        # Detail URL
        # -------------------------------------

        source_url = None

        link = cols[7].find("a")

        if link:

            href = link.get("href")

            if href:

                if href.startswith("http"):
                    source_url = href
                else:
                    source_url = "https://ppra.org.pk" + href

        # -------------------------------------
        # Standard Object
        # -------------------------------------

        tender = {

            "tender_no": tender_no,
            "title": title,

            "category": category,

            "organization": organization_name or organization,

            "department": department,

            "location": location,

            "status": status,

            "publish_date": publish_date,

            "closing_date": closing_date,

            "source_url": source_url,

            "documents": []

        }

        return tender