from fastapi import FastAPI
from fastapi.openapi.models import Tag


class App(FastAPI):
    "Class to generate fast api app."

    API_TITLE = "Brewery System API"
    VERSION = "1.0.0"
    DESCRIPTION = "API's created to manage the sales of a brewery."
    OPEN_API_JSON_URL = "/swagger/openapi.json"
    SWAGGER_URL = "/swagger"

    def __init__(self):
        super().__init__(
            title=self.API_TITLE,
            description=self.DESCRIPTION,
            version=self.VERSION,
            openapi_url=self.OPEN_API_JSON_URL,
            docs_url=self.SWAGGER_URL,
        )
        Tag(
            name="Documentation",
            description="Documentation selection: Swagger.",
        )
        Tag(
            name="Beer",
            description="Beer data control routes.",
        )
        Tag(
            name="Client",
            description="Client data control routes.",
        )
        Tag(
            name="Sales",
            description="Sales data control routes.",
        )


app = App()
