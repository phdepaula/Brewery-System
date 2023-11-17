from pydantic import BaseModel

from database.model.Client import Client


class AddClientSchema(BaseModel):
    """
    Defines how the adding structure \
    in the client database should be.
    """

    name: str
    email: str
    phone: str


class DeleteClientSchema(BaseModel):
    """
    Defines how the delete structure \
    in the client database should be.
    """

    name: str


class UpdateClientSchema(BaseModel):
    """
    Defines how the update structure \
    in the client database should be.
    """

    name: str
    new_value: str


def format_client_data(client: Client) -> dict:
    """
    Format the API response for a added client.
    """
    client_data = {
        "name": client.name,
        "email": client.email,
        "phone": client.phone,
    }

    return client_data
