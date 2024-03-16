from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    intervals: str = Field("5", env="INTERVALS")
    bootstrap_servers: str = Field("localhost:9092", env="BOOTSTRAP_SERVERS")
    topic: str = Field("test", env="SEND_DATA_TOPIC")
    id: str = Field("123", env="ID")


settings = Settings()
