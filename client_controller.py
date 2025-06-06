from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from client_dao import Base, ClientDAO

class ClientController:
    def __init__(self):
        load_dotenv()
        MYSQL_USER = os.getenv("MYSQL_USER")
        MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        MYSQL_HOST = os.getenv("MYSQL_HOST")
        MYSQL_PORT = os.getenv("MYSQL_PORT")
        MYSQL_DB = os.getenv("MYSQL_DB")

        url = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        self.engine = create_engine(url, echo=True, future=True)
        Base.metadata.create_all(self.engine)

    def add_client(self, clientDAO):
        with Session(self.engine) as session:
            new_client = ClientDAO(
                name=clientDAO.name,
                address=clientDAO.address,
                email_address=clientDAO.email_address,
                phone_number=clientDAO.phone_number
            )
            session.add(new_client)
            session.commit()

    def search_client(self, field, query):
        with Session(self.engine) as session:
            clients = ClientDAO.search_client(session, field, query)
            message = ""
            for client in clients:
                message += f"{client}\n"
            return message