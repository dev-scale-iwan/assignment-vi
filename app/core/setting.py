from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    APP_NAME: str = "Assignment 6"
    VERSION: str = "0.0.1"
    
    
settings = Settings()