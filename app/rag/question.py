from app.services.embedding_service import EmbeddingService
from app.services.filter_service import FilterService
from app.services.vector_service import VectorService
from app.services.query_parser import QueryParser
from app.services.llm.context_builder import ContextBuilder
from app.services.llm.groq_service import GroqService
def main():
    embedding_service = EmbeddingService()
    vector_service = VectorService()
    query_parser=QueryParser()
    context_builder=ContextBuilder()
    llm=GroqService()
    

    question = (
        "Tenders for Cyber Security in Karachi"
    )
    parse_query= query_parser.parse(question)
    semantic_query=parse_query["semantic_query"]
    
    



    # Generate embedding
    query_vector = embedding_service.generate_embeddings(semantic_query)

    # Let VectorService.search() handle conversion and normalization
    results = vector_service.search(
        query_embedding=query_vector,
        top_k=100
    )

    if not results:
        print("No matching tenders found.")
        return

    filter_service = FilterService()
    results = filter_service.filter_tenders(
        results=results,
        parsed_query=parse_query
    )
#     results = reranker.rerank(
#     question,
#     results
# )
    
    
    context=context_builder.build(results[:25])
    
    answer=llm.answer(question,context)
    print(answer)
    # results = results[:5]
    # print(f"\nQuestion:\n{question}\n")
    # print("=" * 100)

    if  len(results)==0:
        print("There is no Related Tender for Your Query. Try with different query with full explanation")
           

    # for i, result in enumerate(results, start=1):
        
    #     print(f"Result {i}")
    #     print("-" * 100)
    #     print(f"Tender ID : {result['tender_id']}")
    #     print(f"Title     : {result['title']}")
    #     print(f"Organization: {result['organization']}")
    #     print(f"Publish Date: {result['publish_date']}")
    #     print(f"Closing Date: {result['closing_date']}")
    #     print(f"Location  : {result['location']}")
    #     print(f"Status    : {result['status']}")


    #     print(f"Score     : {result['score']:.4f}")




        print("=" * 100)


if __name__ == "__main__":
    main()