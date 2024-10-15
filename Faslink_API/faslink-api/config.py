from pydantic_settings import BaseSettings, SettingsConfigDict
import pyodbc

class Settings(BaseSettings):
    app_name: str = "Faslink API"
    admin_email: str
    items_per_user: int = 8000

    db_username: str
    db_password: str
    db_host: str
    db_database: str

    model_config = SettingsConfigDict(env_file=".env")