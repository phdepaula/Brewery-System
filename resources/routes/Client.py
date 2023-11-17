from fastapi import HTTPException

from database.model.Client import Client
from database.model.Sales import Sales
from resources.schemas.Client import (AddClientSchema, DeleteClientSchema,
                                      UpdateClientSchema, format_client_data)
from resources.settings.App import app
from resources.util.TableHandler import TableHandler


@app.get(
    "/get_client/{name}",
    tags=["Client"],
)
def get_client(name: str) -> dict:
    """Route to get all the data for a specific client."""
    try:
        client_data = TableHandler().select_data_table(
            table=Client, filter_select={Client.name: name.title()}
        )
        quantity_client = len(client_data)

        if quantity_client > 0:
            message = f"The client {name} was found."
            client_data_json = format_client_data(client_data[0])
        else:
            message = f"The client {name} was not found."
            client_data_json = {}

        response = {"message": message, "client": client_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post(
    "/add_client",
    tags=["Client"],
)
def add_client(form: AddClientSchema) -> dict:
    """Route to add a client in the database."""

    name = (form.name).strip().title()
    email = form.email
    phone = form.phone

    try:
        if len(name) == 0:
            raise Exception("A name must be provided.")

        if email == 0:
            raise Exception("The email must be provided.")

        registered_name = TableHandler().select_value_table_parameter(
            column=Client.name, filter_select={Client.name: name}
        )

        if len(registered_name) > 0:
            raise Exception("Client already registered.")

        new_client = Client(name=name, email=email, phone=phone)
        client_data_json = format_client_data(new_client)
        message = f"The client {name} was added."

        TableHandler().insert_data_table(new_client)

        response = {"message": message, "client": client_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.delete(
    "/delete_client",
    tags=["Client"],
)
def delete_client(form: DeleteClientSchema) -> dict:
    """Route to delete a client in the database."""
    name = (form.name).strip().title()

    try:
        if len(name) == 0:
            raise Exception("A name must be provided.")

        registered_client = TableHandler().select_value_table_parameter(
            column=Client.name, filter_select={Client.name: name}
        )

        if len(registered_client) == 0:
            raise Exception("Client is not registered to be deleted.")

        client_id = TableHandler().select_value_table_parameter(
            column=Client.id, filter_select={Client.name: name}
        )
        registered_sale = TableHandler().select_value_table_parameter(
            column=Sales.name, filter_select={Sales.client_id: client_id}
        )

        if len(registered_sale) != 0:
            raise Exception(
                f"There is already a purchase for {name}, "
                + "it is not possible to delete it."
            )

        TableHandler().delete_data_table(
            table=Client, filter_delete={Client.name: name}
        )

        message = f"The client {name} was deleted."
        client_data_json = {"name": name}

        response = {"message": message, "client": client_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.put(
    "/update_phone_client",
    tags=["Client"],
)
def update_phone_client(form: UpdateClientSchema) -> dict:
    """Route to update a client in the database."""
    name = (form.name).strip().title()
    new_value = (form.new_value).strip().capitalize()

    try:
        if len(name) == 0:
            raise Exception("A name must be provided.")

        registered_client = TableHandler().select_value_table_parameter(
            column=Client.name, filter_select={Client.name: name}
        )

        if len(registered_client) == 0:
            raise Exception("Client is not registered to be updated.")

        old_value = TableHandler().select_value_table_parameter(
            column=Client.phone, filter_select={Client.name: name}
        )
        message = f"The client {name} was updated."
        cient_data_json = {
            "name": name, "old_value": old_value, "new_value": new_value
        }

        TableHandler().update_data_table(
            table=Client,
            filter_update={Client.name: name},
            new_data={Client.phone: new_value},
        )

        response = {"message": message, "client": cient_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
