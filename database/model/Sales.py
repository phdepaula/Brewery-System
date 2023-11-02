from decimal import Decimal

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        func)
from sqlalchemy.orm import relationship

from resources.settings.Database import database


class Sales(database.BASE):
    """Class to create the sales table"""

    __tablename__ = "sales"

    id = Column("sales_id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime, default=func.current_timestamp())
    beer_id = Column(Integer, ForeignKey("beer.beer_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)

    beer = relationship("Beer", back_populates="sales")
    client = relationship("Client", back_populates="sales")

    def __init__(
        self, name: str,
        quantity: int,
        price: float,
        beer_id: int,
        client_id: int
    ):
        self.name = name
        self.quantity = quantity
        self.price = Decimal(price)
        self.beer_id = beer_id
        self.client_id = client_id
