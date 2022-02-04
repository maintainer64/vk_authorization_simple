import pydantic

from runner.configs.environment_avaliable import EnvironmentAvaliable


class ConfigApp(pydantic.BaseSettings):
    access_secret: str
    access_secret_expires: int
    domain: str
    db_name: str
    db_user: str
    db_host: str
    db_port: int
    db_password: str
    sentry_url: str
    environment: EnvironmentAvaliable
    is_docker: bool

    class Config:
        extra = "ignore"
