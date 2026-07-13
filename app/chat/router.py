from dataclasses import dataclass

from app.services.llm.groq_service import GroqService


@dataclass
class RouteDecision:

    action: str

    reason: str = ""


class Router:

    def __init__(self):

        self.llm = GroqService()

    def route(
        self,
        history,
        documents,
        question
    ):

        result = self.llm.route(

            history,

            documents,

            question

        ).upper()

        if "HISTORY" in result:

            return RouteDecision(
                action="HISTORY"
            )

        return RouteDecision(
            action="SEARCH"
        )