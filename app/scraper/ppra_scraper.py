import requests
from bs4 import BeautifulSoup


class PPRAScraper:

    
    BASE_URL = "https://epms.ppra.gov.pk/public/tenders/active-tenders?keyword=&tender_no=&closing_date=&tender_type=&procurement_category=&sector=&tender_nature=&organization=&country=&advertise_date_from=&advertise_date_to=&status=&city=Karachi"

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        })

    def fetch(self, url: str) -> BeautifulSoup:
        """
        Download a page and return BeautifulSoup object.
        """

        response = self.session.get(url, timeout=30)
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

    def get_rows(self, table):
        """
        Return all data rows (skip header).
        """

        rows = table.find_all("tr")

        if len(rows) <= 1:
            return []

        return rows[1:]

    def scrape(self, url):
        """
        Complete scraping process.

        Returns:
            list[Tag]
        """

        soup = self.fetch(url)

        table = self.get_table(soup)

        rows = self.get_rows(table)

        return rows