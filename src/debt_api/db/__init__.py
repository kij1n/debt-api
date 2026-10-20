import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from debt_api.db.models import Base

load_dotenv()

db_pass = os.getenv("POSTGRES_PASSWORD")
if db_pass is None:
    raise ValueError("Password must not be empty")

db_port = os.getenv("POSTGRES_PORT", "5432")
db_user = os.getenv("POSTGRES_USER", "postgres")
db_name = os.getenv("POSTGRES_DB", "postgres")
db_server = os.getenv("POSTGRES_SERVER", "localhost")

url = URL.create(
    "postgresql+psycopg",
    password=db_pass,
    port=db_port,
    username=db_name,
    database=db_name,
    host=db_server,
)

engine = create_engine(url)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
