import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine


BACKEND_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    dotenv_path=BACKEND_DIR / ".env",
    interpolate=False,
)

database_url = URL.create(
    drivername="mysql+pymysql",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
    query={"charset": "utf8mb4"},
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 5},
)