from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    def answer(
        self,
        question: str,
        context: str
    ) -> str:
        pass