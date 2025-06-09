from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer


class Base(DeclarativeBase):
    pass


class ClientDAO(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    email_address = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)

    def __repr__(self):
        return f"""
        Client: {self.name}
        Address: {self.address}
        Email Address: {self.email_address}
        Phone: {self.phone_number}
        """