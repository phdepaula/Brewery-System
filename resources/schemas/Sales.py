from pydantic import BaseModel

from database.model.Sales import Sales


class AddSaleSchema(BaseModel):
    """
    Defines how the adding structure \
    in the sale database should be.
    """

    name_beer: str
    quantity: int
    name_client: str


class DeleteSaleSchema(BaseModel):
    """
    Defines how the delete structure \
    in the sale database should be.
    """

    sales_id: int


class UpdateSaleSchema(BaseModel):
    """
    Defines how the update structure \
    in the sale database should be.
    """

    sales_id: int
    new_quantity: int


def format_sale_data(sale: Sales) -> dict:
    """
    Format the API response for a added sale.
    """
    sale_data = {
        "name": sale.name,
        "quantity": sale.quantity,
        "price": sale.price,
        "beer_id": sale.beer_id,
        "client_id": sale.client_id,
    }

    return sale_data
