from typing import Optional

from app.chat.retrieval_context import RetrievalContext


class ContextManager:

    def __init__(self):

        self._context: Optional[RetrievalContext] = None
        print(self._context)

    @property
    def context(self):

        return self._context

    @property
    def documents(self):

        if self._context is None:
            return []

        return self._context.documents

    @property
    def query(self):

        if self._context is None:
            return None

        return self._context.query

    @property
    def prompt_context(self):

        if self._context is None:
            return ""

        return self._context.prompt_context

    def update(
        self,
        query,
        documents,
        prompt_context
    ):

        self._context = RetrievalContext(
            query=query,
            documents=list(documents),
            prompt_context=prompt_context
        )

    def clear(self):

        self._context = None

    def has_context(self):

        return self._context is not None