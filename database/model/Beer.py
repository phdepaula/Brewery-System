from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from resources.settings.Database import database


class Beer(database.BASE):
    """Class to create the beer table"""

    __tablename__ = "beer"

    beer_id = Column("beer_id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    alcohol_content = Column(Float)
    description = Column(String)
    price = Column(Float, nullable=False)

    sales = relationship("Sales", back_populates="beer")

    def __init__(
        self, name: str, alcohol_content: float, description: str, price: float
    ):
        self.name = name
        self.alcohol_content = float("{:.2%}".format(alcohol_content))
        self.description = description
        self.price = float("{:.2%}".format(price))
