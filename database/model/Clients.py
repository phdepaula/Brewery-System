from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.Settings import database


class Clients(database.BASE):
    """Class to create the clients table"""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(20))
    beer_id = Column(Integer, ForeignKey("beer.id"))

    beer = relationship("Beer", back_populates="clients")

    def __init__(self, name: str, email: str, phone: str, beer_id: int):
        self.name = name
        self.email = email
        self.phone = phone
        self.beer_id = beer_id
