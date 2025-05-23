from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    LLM_MODEL_NAME: str = "gpt-4o-mini"
    LLM_MAX_TOKENS: int = 10000
    LLM_TEMPERATURE: float = 0.1

    # If you have a .env file, this will load it.
    # For pydantic-settings v2.x.x
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')
    # For pydantic-settings v1.x.x (if needed, but prefer v2)
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = 'utf-8'
    #     extra = 'ignore'

settings = Settings()
