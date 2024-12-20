import os
from typing import Iterator
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationResponse, FunctionDeclaration, Tool, Part
import requests

from .llm_interface import LLMInterface

class LLM(LLMInterface):
    def __init__(
        self,
        system: str = None,
        project: str = None,
        location: str = None,
        model: str = None,
    ):
        vertexai.init(
            project=project,
            location=location,
        )

        places_search = FunctionDeclaration(
            name="places_search",
            description="Get information about places and points of interest.",
            parameters={
                "type": "object",
                "properties": {
                    "textQuery": { "type": "string" }
                },
            }
        )

        get_products = FunctionDeclaration(
            name="get_products",
            description="when user ask about product in `myshop` use this function",
            parameters={
                "type": "object",
                "properties": {
                },
            }
        )

        chat_tool = Tool(
            function_declarations=[places_search, get_products],
        )

        self.model = GenerativeModel(
            model_name=model,
            system_instruction=system if system else "",
            tools=[chat_tool],
        )

        self.chat =  self.model.start_chat()


    def chat_iter(self, prompt: str) -> Iterator[str]:
        try:
            res = self.chat.send_message(
                content=prompt,
                # stream=True,
            )

            yield from self._process_response(res)

        except Exception as e:
            print(f"Error calling Vertex AI: {str(e)}")
            return iter([f"Error calling Vertex AI: {str(e)}"])


    def _process_response(self, response: GenerationResponse) -> Iterator[str]:
        for part in response.candidates[0].content.parts:
            if part.function_call is not None:
                if part.function_call.name == "get_products":
                    products = self._search_myshop()
                    res = self.chat.send_message(
                        Part.from_function_response(
                            name="get_products",
                            response={"content": products}
                        )
                    )
                else:
                    print (part)
                    places = self._search_places(part.function_call.args["textQuery"])

                    res = self.chat.send_message(
                        Part.from_function_response(
                            name="places_search",
                            response={"content": places}
                        )
                    )

                yield from self._process_response(res)
            else:
                yield from self._process_text_response(part)


    def _process_text_response(self, part: Part) -> Iterator[str]:
        sentences = part.text.split("\n")

        for s in sentences:
            if s != "": yield s


    def _search_places(self, text_query: str) -> list[dict]:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        res = requests.post(
            "https://places.googleapis.com/v1/places:searchText",
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": google_api_key,
                "X-Goog-FieldMask": "places.displayName"
            },
            json={"textQuery": text_query},
        )

        return res.json()

    def _search_myshop(self) -> dict:
        api_key = os.getenv("LINE_SHOPPING_API_KEY")
        res = requests.get(
            "https://developers-oaplus.line.biz/myshop/v1/products", 
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "user-agent": "python",
            },
        )

        return res.json()


    def handle_interrupt(self, heard_response):
        print("Interrupted")