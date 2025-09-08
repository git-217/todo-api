from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings():
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings() #type: ignore

def get_asyncpg_db_url():
    return (f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@'
            f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')