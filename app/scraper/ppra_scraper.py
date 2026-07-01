import requests
from bs4 import BeautifulSoup
import re

class PPRAScraper:

    
    BASE_URL = "https://epms.ppra.gov.pk/public/tenders/active-tenders"
    DEFAULT_PARAMS = {
    "keyword": "",
    "tender_no": "",
    "closing_date": "",
    "tender_type": "",
    "procurement_category": "",
    "sector": "",
    "tender_nature": "",
    "organization": "",
    "country": "",
    "advertise_date_from": "",
    "advertise_date_to": "",
    "status": "",
    "city": "",
                    }


    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        })

    def fetch(self, page=1):

        params = self.DEFAULT_PARAMS.copy()
        params["page"] = page

        response = self.session.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return BeautifulSoup(response.text, "html.parser")        
    def get_table(self, soup: BeautifulSoup):
        """
        Find the tender table.
        """

        table = soup.find(
            "table",
            class_="table table-hover mb-0"
        )

        if table is None:
            raise Exception("Tender table not found.")

        return table
    def get_total_pages(self, soup):

        text = soup.get_text(" ", strip=True)

        match = re.search(r"Page\s+\d+\s+of\s+(\d+)", text)

        if match:
            return int(match.group(1))

        return 1
    def get_rows(self, table):
        """
        Return all data rows (skip header).
        """

        rows = table.find_all("tr")

        if len(rows) <= 1:
            return []

        return rows[1:]

    def scrape(self):

        first_page = self.fetch(page=1)

        total_pages = self.get_total_pages(first_page)

        print(f"Total Pages: {total_pages}")

        all_rows = []

        for page in range(1, total_pages + 1):

            print(f"Scraping Page {page}")

            soup = self.fetch(page)

            table = self.get_table(soup)

            rows = self.get_rows(table)

            all_rows.extend(rows)

        return all_rows