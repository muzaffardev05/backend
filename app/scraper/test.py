from app.scraper.ppra_scraper import PPRAScraper
from app.scraper.ppra_parser import PPRAParser
from app.services.database_service import DatabaseService
from app.services.document_service import DocumentService
from app.rag.chunker import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
embedding_service = EmbeddingService()
db = DatabaseService()
scraper = PPRAScraper()
document_service = DocumentService()
chunk_service=ChunkService()
vector_service = VectorService()
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
    print(chunks[1:3])
    texts = [chunk["text"] for chunk in chunks]
    chunks = db.get_unembedded_chunks()
    print(f"Pending chunks: {len(chunks)}")
    batch_size = 64
    for i in range(0, len(chunks), batch_size):

        batch = chunks[i:i + batch_size]

        texts = [chunk["text"] for chunk in batch]

        embeddings = embedding_service.generate_embeddings(texts)
        vector_service.add_vectors(batch, embeddings)
        
        for chunk in batch:
            db.mark_chunk_as_embedded(chunk["id"])
            print(f"Chunk {chunk['tender_id']} - {chunk['chunk_index']} marked as embedded.")
            print(f"Embedded batch {i // batch_size + 1}")



