from app.services.embedding_service import EmbeddingService
from app.services.filter_service import FilterService
from app.services.vector_service import VectorService


def main():
    embedding_service = EmbeddingService()
    vector_service = VectorService()

    question = (
        "Tenders for network firewalls, intrusion detection systems (IDS), and core switch security upgrades"
    )

    # Generate embedding
    query_vector = embedding_service.generate_embeddings(question)

    # Let VectorService.search() handle conversion and normalization
    results = vector_service.search(
        query_embedding=query_vector,
        top_k=5
    )

    if not results:
        print("No matching tenders found.")
        return

    filter_service = FilterService()
    results = filter_service.filter_tenders(
        results=results,
        question=question
    )
    results = results[:5]
    print(f"\nQuestion:\n{question}\n")
    print("=" * 100)



    for i, result in enumerate(results, start=1):
        
        print(f"Result {i}")
        print("-" * 100)
        print(f"Tender ID : {result['tender_id']}")
        print(f"Title     : {result['title']}")
        print(f"Organization: {result['organization']}")
        print(f"Publish Date: {result['publish_date']}")
        print(f"Closing Date: {result['closing_date']}")
        print(f"Location  : {result['location']}")
        print(f"Status    : {result['status']}")


        print(f"Score     : {result['score']:.4f}")




        print("=" * 100)


if __name__ == "__main__":
    main()