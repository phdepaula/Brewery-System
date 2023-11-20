import os

import uvicorn

import resources.routes.Beer
import resources.routes.Client
import resources.routes.Documentation
import resources.routes.Sales
from resources.settings.App import app
from resources.settings.Database import database

if __name__ == "__main__":
    database.setup_database_environment()
    uvicorn.run(app, host="localhost", port=8000)
