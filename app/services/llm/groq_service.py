import os

from groq import Groq
from dotenv import load_dotenv
from app.services.llm.base import BaseLLM
from app.services.llm.prompt_builder import SYSTEM_PROMPT
load_dotenv()


class GroqService(BaseLLM):

    def __init__(self):

        self.client = Groq(

            api_key=os.getenv(
                "GROQ_API_KEY"
            )

        )

    def answer(

        self,

        question,

        context,

    ):

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0,

            messages=[

                {

                    "role": "system",

                    "content": SYSTEM_PROMPT

                },

                {

                    "role": "user",

                    "content":
f"""
Question

{question}

Retrieved Tenders

{context}
"""

                }

            ]

        )

        return response.choices[0].message.content