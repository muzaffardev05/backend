from app.scraper.ppra_scraper import PPRAScraper
from app.scraper.ppra_parser import PPRAParser
from app.services.database_service import DatabaseService
from app.services.document_service import DocumentService
from app.rag.chunker import ChunkService
db = DatabaseService()
scraper = PPRAScraper()
document_service = DocumentService()
chunk_service=ChunkService()
rows = scraper.scrape()

print(f"Total tenders: {len(rows)}")

parser = PPRAParser()
documents = []
for row in rows:

    tender = parser.parse(row)
    
    document = document_service.build_document(tender)
    documents.append({
        "tender_id": tender["tender_no"],
        "text": document
    })

    db.save_tender(tender)
    


if(documents):
    chunks = chunk_service.chunk_documents(documents)
    db.save_chunks(chunks)
    print(f"Total chunks: {len(chunks)}")
    print(chunks[1:12])
