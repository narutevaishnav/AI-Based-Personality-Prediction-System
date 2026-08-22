import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import db

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)
if not DATABASE_URL:
    raise Exception(
        "DATABASE_URL not found in .env"
    )

# -----------------------------
# SQLAlchemy Engine
# -----------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_reset_on_return="commit"
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

## -----------------------------
# Initialize Database
# -----------------------------
def init_db(app):

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():

        try:

            db.create_all()

            print("PostgreSQL Connected Successfully!")
            print("Tables Created Successfully!")

        except Exception as e:

            print("DATABASE ERROR:")
            print(repr(e))

            raise
        print("DATABASE_URL =", DATABASE_URL)