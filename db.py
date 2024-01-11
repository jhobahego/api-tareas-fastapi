from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from decouple import config


engine = create_engine(config('DB_URL_CONNECTION'), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
