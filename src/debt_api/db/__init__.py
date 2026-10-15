import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

load_dotenv()

db_pass = os.getenv("POSTGRES_PASSWORD")
if db_pass is None:
    raise ValueError("Password must not be emty")

db_port = os.getenv("POSTGRES_PORT", "5432")
db_user = os.getenv("POSTGRES_USER", "postgres")
db_name = os.getenv("POSTGRES_DB", "postgres")

url = URL(
    "postgres+psycopg2",
    password=db_pass,
    port=db_port,
    username=db_name,
    database=db_name,
)

engine = create_engine(url)
session = Session(engine)
