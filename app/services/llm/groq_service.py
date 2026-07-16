import os

from groq import Groq
from dotenv import load_dotenv

from app.services.llm.base import BaseLLM
from app.services.llm.router_prompt import ROUTER_PROMPT
from app.services.llm.prompt_builder import SYSTEM_PROMPT

load_dotenv()


class GroqService(BaseLLM):

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    def _complete(
        self,
        system_prompt,
        user_prompt,
        temperature=0
    ):

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=temperature,

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }

            ]

        )

        return response.choices[0].message.content.strip()


    def answer(
        self,
        question,
        context
    ):

        return self._complete(

            system_prompt=SYSTEM_PROMPT,

            user_prompt=f"""
Question

{question}

Retrieved Tenders

{context}
"""
        )
    



    def route(
    self,
    history,
    documents,
    question
):

        prompt = f"""
    Conversation

    {history}

    Retrieved Documents

    {documents}

    Question

    {question}
    """

        return self._complete(

            system_prompt=ROUTER_PROMPT,

            user_prompt=prompt
        )  