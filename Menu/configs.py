import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "grand_central"
    PROJECT_ROOT: pathlib.Path = pathlib.Path(__file__).parent
    PACT_DIR: str = f"{PROJECT_ROOT.parent}/tests/pacts/"
    DEBUG: bool = False


settings = Settings()
