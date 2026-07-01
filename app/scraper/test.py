from app.scraper.ppra_scraper import PPRAScraper
from app.scraper.ppra_parser import PPRAParser
from app.services.database_service import DatabaseService

db = DatabaseService()
scraper = PPRAScraper()

rows = scraper.scrape()

print(f"Total tenders: {len(rows)}")

parser = PPRAParser()

for row in rows:

    tender = parser.parse(row)


    db.save_tender(tender)

    print(tender)