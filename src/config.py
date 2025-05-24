from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    pg_dsn: str
    api_host: str
    api_port: int
    gis_api: str
    api_ya_geocode: str

    model_config = SettingsConfigDict(env_file='.conf', env_file_encoding='utf-8')
