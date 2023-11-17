from fastapi import HTTPException

from database.model.Beer import Beer
from database.model.Sales import Sales
from resources.schemas.Beer import (AddBeerSchema, DeleteBeerSchema,
                                    UpdateBeerSchema, format_beer_data)
from resources.settings.App import app
from resources.util.TableHandler import TableHandler


@app.get(
    "/get_beer/{name}",
    tags=["Beer"],
)
def get_beer(name: str) -> dict:
    """Route to get all the data for a specific beer."""
    try:
        beer_data = TableHandler().select_data_table(
            table=Beer, filter_select={Beer.name: name.title()}
        )
        quantity_beer = len(beer_data)

        if quantity_beer > 0:
            message = f"The beer {name} was found."
            beer_data_json = format_beer_data(beer_data[0])
        else:
            message = f"The beer {name} was not found."
            beer_data_json = {}

        response = {"message": message, "beer": beer_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post(
    "/add_beer",
    tags=["Beer"],
)
def add_beer(form: AddBeerSchema) -> dict:
    """Route to add a beer in the database."""

    name = (form.name).strip().title()
    alcohol_content = form.alcohol_content
    description = (form.description).strip()
    price = form.price

    try:
        if len(name) == 0:
            raise Exception("A name must be provided.")

        if price == 0:
            raise Exception("The price must be greater than zero.")

        registered_beer = TableHandler().select_value_table_parameter(
            column=Beer.name, filter_select={Beer.name: name}
        )

        if len(registered_beer) > 0:
            raise Exception("Beer already registered.")

        new_beer = Beer(
            name=name,
            alcohol_content=alcohol_content,
            description=description,
            price=price,
        )
        beer_data_json = format_beer_data(new_beer)
        message = f"The beer {name} was added."

        TableHandler().insert_data_table(new_beer)

        response = {"message": message, "beer": beer_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.delete(
    "/delete_beer",
    tags=["Beer"],
)
def delete_beer(form: DeleteBeerSchema) -> dict:
    """Route to delete a beer in the database."""
    name = (form.name).strip().title()

    try:
        if len(name) == 0:
            raise Exception("A name must be provided.")

        registered_beer = TableHandler().select_value_table_parameter(
            column=Beer.name, filter_select={Beer.name: name}
        )

        if len(registered_beer) == 0:
            raise Exception("Beer is not registered to be deleted.")

        registered_sale = TableHandler().select_value_table_parameter(
            column=Sales.name, filter_select={Sales.name: name}
        )

        if len(registered_sale) != 0:
            raise Exception(
                "Beer has already been sold, it is not possible to delete it."
            )

        TableHandler().delete_data_table(
            table=Beer, filter_delete={Beer.name: name}
        )

        message = f"The beer {name} was deleted."
        beer_data_json = {"name": name}

        response = {"message": message, "beer": beer_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.put(
    "/update_description_beer",
    tags=["Beer"],
)
def update_beer(form: UpdateBeerSchema) -> dict:
    """Route to update a beer in the database."""
    name = (form.name).strip().title()
    new_value = (form.new_value).strip().capitalize()

    try:
        if len(name) == 0:
            raise Exception("A name must be provided.")

        registered_beer = TableHandler().select_value_table_parameter(
            column=Beer.name, filter_select={Beer.name: name}
        )

        if len(registered_beer) == 0:
            raise Exception("Beer is not registered to be updated.")

        old_value = TableHandler().select_value_table_parameter(
            column=Beer.description, filter_select={Beer.name: name}
        )
        message = f"The beer {name} was updated."
        beer_data_json = {
            "name": name, "old_value": old_value, "new_value": new_value
        }

        TableHandler().update_data_table(
            table=Beer,
            filter_update={Beer.name: name},
            new_data={Beer.description: new_value},
        )

        response = {"message": message, "beer": beer_data_json}
        return response
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
