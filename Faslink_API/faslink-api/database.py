from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser
import sqlalchemy as engine
from . import config
from functools import lru_cache
from dotenv import load_dotenv  # Thêm dòng này
import os

# Nạp tệp .env
load_dotenv()  # Thêm dòng này

@lru_cache
def get_settings():
    return config.Settings()

SQLALCHEMY_DATABASE_URL = engine.URL.create(
    "mssql+pyodbc",
    username=get_settings().db_username,
    password=get_settings().db_password,
    host=get_settings().db_host,
    database=get_settings().db_database,
    query={"driver": "ODBC Driver 17 for SQL Server"},  # Chuyển về đúng driver
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    deprecate_large_types=True, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
