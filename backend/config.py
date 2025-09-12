from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings() #type: ignore

def get_asyncpg_db_url():
    return (f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@'
            f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')

def get_auth_data():
    return {'secret_key': settings.SECRET_KEY, 'algorithm': settings.ALGORITHM}