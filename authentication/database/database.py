"""_database."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@postgres_authentication:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """_summary_

    Yields:
        _type_: _description_
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close  # pylint: disable=pointless-statement
