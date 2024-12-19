import abc
from typing import Iterator


class ProductInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_products(self) -> str:
        """
        Sends a api request to get products and return an iterator to the response.

        Parameters:

        Returns:
        - Iterator[str]: An iterator to the response from the product provider.
        """
        raise NotImplementedError
