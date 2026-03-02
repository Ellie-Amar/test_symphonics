from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://user:password@localhost:5432/app"
    command_log_path: str = "./var/commands.jsonl"
    bigquery_log_path: str = "./var/bigquery.jsonl"
    power_threshold: float = 2000

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


def get_settings() -> Settings:
    return Settings()
