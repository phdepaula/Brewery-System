from typing import Any, Dict, Union

from fastapi import HTTPException

from database.model.Beer import Beer
from resources.schemas.Beer import (AddBeerSchema, BeerSchema, MessageSchema,
                                    format_beer_data)
from resources.settings.App import app
from resources.util.TableHandler import TableHandler


@app.get(
    "/get_beer/{name}",
    tags=["Beer"],
    response_model=BeerSchema,
    responses={
        200: {"model": BeerSchema},
        400: {"model": MessageSchema},
    },
)
def get_beer(name: str) -> Union[
    Dict[str, str], Dict[str, Union[str, Dict[str, Any]]]
]:
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
    response_model=BeerSchema,
    responses={
        200: {"model": BeerSchema},
        400: {"model": MessageSchema},
    },
)
def add_beer(
    form: AddBeerSchema,
) -> Union[Dict[str, str], Dict[str, Union[str, Dict[str, Any]]]]:
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

        registered_product = TableHandler().select_value_table_parameter(
            column=Beer.name, filter_select={Beer.name: name}
        )

        if len(registered_product) > 0:
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
