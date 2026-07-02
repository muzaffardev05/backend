from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


def main():
    embedding_service = EmbeddingService()
    vector_service = VectorService()

    question = "Show me IT tenders"

    # Generate embedding
    query_vector = embedding_service.generate_embedding(question)

    # Search vector database
    results = vector_service.search(
        query_embedding=query_vector,
        top_k=5
    )

    if not results:
        print("No matching tenders found.")
        return

    print(f"\nQuestion: {question}\n")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        print(f"Result {i}")
        print("-" * 80)
        print(f"Tender ID  : {result['tender_id']}")
        print(f"Score      : {result['score']:.4f}")
        print(f"Chunk      : {result['chunk_index']}")
        print("Text:")
        print(result["text"])
        print("=" * 80)


if __name__ == "__main__":
    main()