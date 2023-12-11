from pathlib import Path
from sys import path

from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(path[0]) / ".env", env_file_encoding="utf-8"
    )

    debug: bool = False

    db_url: str = Field(default_factory=str)
    default_link: str = (
        "https://www.citilink.ru/product/mysh-oklick-605sw-opticheskaya-besprovodnaya-usb-chernyi-i-sinii-wm-28-384109/"
    )
