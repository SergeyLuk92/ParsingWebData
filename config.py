# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    domain_url: str
    num_pages: int
    output_dir: str
    csv_file_name: str

    class Config:
        env_file = ".env"

settings = Settings()
