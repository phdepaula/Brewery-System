from database.model.Database import Database

HOST = "localhost:5432"
DATABASE_NAME = "Brewery"
USER = "postgres"
PASSWORD = "senha"

SETTINGS = {
    "host": HOST,
    "database": DATABASE_NAME,
    "user": USER,
    "password": PASSWORD
}

database = Database(SETTINGS)
