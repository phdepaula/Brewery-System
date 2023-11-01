from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.Settings import database


class Client(database.BASE):
    """Class to create the clients table"""

    __tablename__ = "client"

    id = Column("client_id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))

    sales = relationship("Sales", back_populates="client")

    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone
