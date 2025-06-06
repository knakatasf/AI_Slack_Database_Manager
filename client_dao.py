from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass
class ClientDAO(Base):
    __tablename__ = "clients"
    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name          = Column(String(255), nullable=False)
    address       = Column(String(255), nullable=False)
    email_address = Column(String(255), nullable=False)
    phone_number  = Column(String(255), nullable=False)

    @classmethod
    def get_by_name(cls, session, name):
        clients = session.query(cls).filter(cls.name.like(f"{name}%")).all()
        return clients

    @classmethod
    def get_by_address(cls, session, address):
        clients = session.query(cls).filter(cls.name.like(f"{address}%")).all()
        return clients

    @classmethod
    def get_by_email_address(cls, session, email_address):
        clients = session.query(cls).filter(cls.name.like(f"{email_address}%")).all()
        return clients

    @classmethod
    def get_by_phone_number(cls, session, phone_number):
        clients = session.query(cls).filter(cls.name.like(f"{phone_number}%")).all()
        return clients

    @classmethod
    def search_client(cls, session: Session, field: int, query: str) -> list["ClientDAO"]:
        # field: 1=name, 2=address, 3=email, 4=phone
        dispatch = {
            1: cls.get_by_name,
            2: cls.get_by_address,
            3: cls.get_by_email_address,
            4: cls.get_by_phone_number,
        }
        func = dispatch.get(field)
        if not func:
            raise ValueError(f"Unknown field {field!r}, must be 1–4")
        return func(session, query)

    def __repr__(self):
        return f"""
        Client: {self.name}
        Address: {self.address}
        Email Address: {self.email_address}
        Phone: {self.phone_number}
        """
