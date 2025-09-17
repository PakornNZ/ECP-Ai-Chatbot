from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_DB = os.getenv("POSTGRES_DB", "ecp-ai")
DATABASE_USER = os.getenv("POSTGRES_USER", "postgres")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pass123")
DATABASE_HOST = os.getenv("POSTGRES_HOST", "database-postgres")
DATABASE_PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]