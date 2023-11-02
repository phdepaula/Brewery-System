from typing import Dict

from pydantic import BaseModel

from database.model.Beer import Beer


class BeerSchema(BaseModel):
    """
    Defines how the API response should be \
    for a successfully completed query for a beer.
    """

    message: str
    beer: Dict


class MessageSchema(BaseModel):
    """
    Defines how the API response should be \
    when you want to send just one message.
    """

    message: str


class AddBeerSchema(BaseModel):
    """
    Defines how the adding structure \
    in the beer database should be.
    """

    name: str
    alcohol_content: float
    description: str
    price: float


def format_beer_data(beer: Beer) -> dict:
    """
    Format the API response for a added product.
    """
    beer_data = {
        "name": beer.name,
        "alcohol_content": beer.alcohol_content,
        "description": beer.description,
        "price": beer.price,
    }

    return beer_data
