import os
from typing import Type
from .product_interface import ProductInterface
from .line_shopping import Product as LINEShopping

class ProductFactory:
    @staticmethod
    def create_product_provider(prodcut_provider, **kwargs) -> Type[ProductInterface]:
        if prodcut_provider == "line_shopping":
            api_key = os.getenv("LINE_SHOPPING_API_KEY", "")
            print("init line shopping " + api_key + "\n")
            return LINEShopping(api_key)