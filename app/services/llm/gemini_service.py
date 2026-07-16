import os

from google import genai
from google.genai.types import GenerateContentConfig


class GeminiService:

    def __init__(
        self,
        model="gemini-3-flash-preview"
    ):
        self.client = genai.Client(
            api_key="APikey"
        )

        self.model = model

    def generate(
        self,
        prompt,
        system_prompt=None,
        temperature=0.2,
        max_tokens=1024
    ):

        contents = []

        if system_prompt:
            contents.append(system_prompt)

        contents.append(prompt)

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )

        return response.text
    





llm = GeminiService()

answer = llm.generate(
    prompt="Conversation Memory  : Vendor Search explain more than 1000 words",
    system_prompt="You are a helpful assistant."
)

print(answer)