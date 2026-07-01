from ppra_scraper import PPRAScraper
from ppra_parser import PPRAParser

URL = "https://epms.ppra.gov.pk/public/tenders/active-tenders?keyword=&tender_no=&closing_date=&tender_type=&procurement_category=&sector=&tender_nature=&organization=&country=&advertise_date_from=&advertise_date_to=&status=&city=Karachi"

scraper = PPRAScraper()

rows = scraper.scrape()

print(f"Total tenders: {len(rows)}")

parser = PPRAParser()

for row in rows:

    tender = parser.parse(row)

    print(tender)