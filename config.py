from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    chai_api_url: str

    model_config = SettingsConfigDict(env_file='.env')