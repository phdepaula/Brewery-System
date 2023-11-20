from fastapi import HTTPException

from database.model.Beer import Beer
from database.model.Client import Client
from database.model.Sales import Sales
from resources.schemas.Sales import (
    AddSaleSchema,
    DeleteSaleSchema,
    UpdateSaleSchema,
    format_sale_data,
)
from resources.settings.App import app
from resources.util.TableHandler import TableHandler


@app.get(
    "/get_sale/{id}",
    tags=["Sales"],
)
def get_sale(id: int) -> dict:
    """Route to get all the data for a specific sale."""
    try:
        sale_data = TableHandler().select_data_table(
            table=Sales, filter_select={Sales.id: id}
        )

        if sale_data != "":
            message = f"The sale {id} was found."
            sale_data_json = format_sale_data(sale_data[0])
            sale_data_json["id"] = id
        else:
            message = f"The sale {id} was not found."
            sale_data_json = {}

        response = {"message": message, "sale": sale_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post(
    "/add_sale",
    tags=["Sales"],
)
def add_sale(form: AddSaleSchema) -> dict:
    """Route to add a sale in the database."""

    name_beer = (form.name_beer).strip().title()
    name_client = (form.name_client).strip().title()
    quantity = int(form.quantity)

    try:
        if len(name_beer) == 0:
            raise Exception("A name must be provided for the beer.")

        if len(name_client) == 0:
            raise Exception("A name must be provided for the client.")

        if quantity == 0:
            raise Exception("The quantity must be greater than zero.")

        beer_id = TableHandler().select_value_table_parameter(
            column=Beer.beer_id, filter_select={Beer.name: name_beer}
        )

        if beer_id == "":
            raise Exception("Beer not registered.")

        client_id = TableHandler().select_value_table_parameter(
            column=Client.id, filter_select={Client.name: name_client}
        )

        if client_id == "":
            raise Exception("Client not registered.")

        beer_price = TableHandler().select_value_table_parameter(
            column=Beer.price, filter_select={Beer.name: name_beer}
        )

        new_sale = Sales(
            name=name_beer,
            quantity=quantity,
            price=beer_price * quantity,
            beer_id=beer_id,
            client_id=client_id,
        )
        sale_data_json = format_sale_data(new_sale)
        message = "The sale was added."

        TableHandler().insert_data_table(new_sale)

        response = {"message": message, "sale": sale_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.delete(
    "/delete_sale",
    tags=["Sales"],
)
def delete_sale(form: DeleteSaleSchema) -> dict:
    """Route to delete a sale in the database."""
    id = int(form.sales_id)

    try:
        sale_id = TableHandler().select_value_table_parameter(
            column=Sales.id, filter_select={Sales.id: id}
        )

        if sale_id == "":
            raise Exception("The sale does not exist.")

        TableHandler().delete_data_table(
            table=Sales,
            filter_delete={Sales.id: id}
        )

        message = f"The sale {id} was deleted."
        sale_data_json = {"sales_id": id}

        response = {"message": message, "sale": sale_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.put(
    "/update_sale_quantity",
    tags=["Sales"],
)
def update_sale(form: UpdateSaleSchema) -> dict:
    """Route to update a sale in the database."""
    id = int(form.sales_id)
    new_quantity = int(form.new_quantity)

    try:
        sale_id = TableHandler().select_value_table_parameter(
            column=Sales.id, filter_select={Sales.id: id}
        )

        if sale_id == "":
            raise Exception("The sale does not exist.")

        if new_quantity == 0:
            raise Exception("The quantity must be greater than zero.")

        old_quantity = TableHandler().select_value_table_parameter(
            column=Sales.quantity, filter_select={Sales.id: id}
        )

        name_beer = TableHandler().select_value_table_parameter(
            column=Sales.name, filter_select={Sales.id: id}
        )

        beer_price = TableHandler().select_value_table_parameter(
            column=Beer.price, filter_select={Beer.name: name_beer}
        )

        TableHandler().update_data_table(
            table=Sales,
            filter_update={Sales.id: id},
            new_data={
                Sales.quantity: new_quantity,
                Sales.price: beer_price * new_quantity,
            },
        )

        message = f"The sale {id} was updated."
        sale_data_json = {
            "sales_id": id,
            "old_quantity": old_quantity,
            "new_quantity": new_quantity,
        }

        response = {"message": message, "sale": sale_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
