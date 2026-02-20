from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Hardcode SQLite for now (no .env needed)
DATABASE_URL = "sqlite:///./riftdb.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
