from pydantic import BaseModel

from database.model.Beer import Beer


class AddBeerSchema(BaseModel):
    """
    Defines how the adding structure \
    in the beer database should be.
    """

    name: str
    alcohol_content: float
    description: str
    price: float


class DeleteBeerSchema(BaseModel):
    """
    Defines how the delete structure \
    in the beer database should be.
    """

    name: str


class UpdateBeerSchema(BaseModel):
    """
    Defines how the update structure \
    in the beer database should be.
    """

    name: str
    new_value: str


def format_beer_data(beer: Beer) -> dict:
    """
    Format the API response for a added beer.
    """
    beer_data = {
        "name": beer.name,
        "alcohol_content": beer.alcohol_content,
        "description": beer.description,
        "price": beer.price,
    }

    return beer_data
