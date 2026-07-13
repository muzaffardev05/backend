from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.filter_service import FilterService
from app.services.query_parser import QueryParser
from app.services.llm.context_builder import ContextBuilder
from app.services.llm.groq_service import GroqService
from app.chat.prompt_builder import PromptBuilder
from app.chat.chat_session import ChatSession
from app.chat.router import Router
class ChatBot:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.vector_service = VectorService()

        self.filter_service = FilterService()

        self.query_parser = QueryParser()

        self.context_builder = ContextBuilder()

        self.llm = GroqService()
        self.chat=ChatSession()
        self.router=Router()
        

    def ask(
        self,
        question: str
    ):
        

        chat =self.chat
        chat.add_user_message(question)
        history=PromptBuilder.history(chat.history)
        if chat.has_context():
            documents=PromptBuilder.documents(
                chat.context.documents
            )
        else:
            documents="No retrived documents"    
        parsed_query = None
        decision=self.router.route(
            history=history,
            documents=documents,
            question=question
        )

        if decision.action=="SEARCH":

            # -----------------------------
            # Parse User Query
            # -----------------------------

            parsed_query = self.query_parser.parse(
                question
            )

            semantic_query = parsed_query[
                "semantic_query"
            ]

            # -----------------------------
            # Generate Embedding
            # -----------------------------

            query_vector = (
                self.embedding_service.generate_embeddings(
                    semantic_query
                )
            )

            # -----------------------------
            # Vector Search
            # -----------------------------

            results = self.vector_service.search(
                query_embedding=query_vector,
                top_k=100
            )

            if not results:

                return {
                    "answer": "No matching tenders found.",
                    "results": []
                }

            # -----------------------------
            # Apply Filters
            # -----------------------------

            results = self.filter_service.filter_tenders(
                results=results,
                parsed_query=parsed_query
            )

            if not results:

                return {
                    "answer": (
                        "There is no related tender "
                        "for your query."
                    ),
                    "results": []
                }

        # -----------------------------
        # Build Context
        # -----------------------------

            context = self.context_builder.build(
                results[:25]
            )

            # -----------------------------
            # Generate Final Answer
            # -----------------------------

            chat.context.update(
                query=question,
                documents=results,
                prompt_context=context
            )
        else:
            results=chat.context.documents
            context=chat.context.prompt_context

        answer = self.llm.answer(
            question,
            context
        )
        chat.add_assistant_message(answer)

        return {
            "answer": answer,
            "results": results,
            "context": context,
            "parsed_query": parsed_query
        }