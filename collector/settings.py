from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    intervals = Field(..., env="INTERVALS")
    bootstrap_servers = Field(..., env="BOOTSTRAP_SERVERS")
    topic = Field(..., env="SEND_DATA_TOPIC")


settings = Settings()
