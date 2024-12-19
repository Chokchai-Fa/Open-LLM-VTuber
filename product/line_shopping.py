import json
import requests

from .product_interface import ProductInterface


class Product(ProductInterface):

    def __init__(
        self,
        api_key,
    ):
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "x-api-key": api_key,
            "user-agent": "python",
        } 
        self.verbose = True

    def get_products(self):
        response = requests.get(
            "https://developers-oaplus.line.biz/myshop/v1/products", 
            headers=self.headers, 
            stream=True, timeout=30
        )

        if response.status_code != 200:
            raise ValueError(f"Failed to send message: {response.text}")

        result = ""

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8").strip()
                if decoded_line.startswith("data:"):
                    decoded_line = decoded_line[len("data:") :].strip()
                if decoded_line:
                    print (decoded_line + "\n\n")
                    result += decoded_line
                    # try:
                    #     json_line = json.loads(decoded_line)
                    #     if self.verbose:
                    #         print(json_line)
                        
                    #     for item in json_line["data"]:
                    #         result += item["name"] + " "

                    # except json.JSONDecodeError as e:
                    #     print(f"Error decoding JSON: {e} for line: {decoded_line}")
                else:
                    print("Received an empty line or non-JSON data.")

        return result

def test():
    llm = Product(
        api_key=os.getenv("LINE_SHOPPING_API_KEY"),
        verbose=True,
    )
    
    products = llm.get_products()
    print (products)


if __name__ == "__main__":
    test()
