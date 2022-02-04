import logging

import sentry_sdk
from fastapi_jsonrpc import Entrypoint

from sentry_asgi import SentryMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from starlette.middleware.cors import CORSMiddleware
from runner.configs import config
from runner.utils.bind_methods import bind_methods_on_router

logger = logging.getLogger(__name__)

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,
    event_level=logging.WARNING,
)

sentry_sdk.init(
    dsn=config.sentry_url,
    environment=config.environment.value,
    integrations=[sentry_logging],
)


async def startup():
    from application.dependencies.application_container import ApplicationDependenciesContainer

    di = await ApplicationDependenciesContainer.create()
    route = Entrypoint("/api/v1/jsonrpc")
    route_methods = await di.create()
    bind_methods_on_router(
        router=route,
        methods_list=route_methods.methods,
    )
    application.state.container = route_methods
    application.bind_entrypoint(route)


def get_app():
    from runner.app import app as _app

    _app.add_middleware(SentryMiddleware)
    origins = [
        "https://localhost:3000",
        "http://localhost:3000",
    ]
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


application = get_app()


@application.on_event("shutdown")
async def shutdown():
    from application.repositories.database.bind import db_manager

    logger.debug("<Application shutdown>")
    await db_manager.close()
    logger.debug("<Application db-disconnected>")


@application.on_event("startup")
async def startup_event():
    await startup()
    if config.environment.LOCAL == config.environment:
        logger.debug("On migrate")
        logger.debug(
            "pw_migrate create --auto --directory application/migrations "
            f"--database postgresql://{config.db_user}:{config.db_password}@"
            f"{config.db_host}:{config.db_port}/{config.db_name}"
        )
        logger.debug(
            "pw_migrate migrate --directory application/migrations"
            f" --database postgresql://{config.db_user}:{config.db_password}@"
            f"{config.db_host}:{config.db_port}/{config.db_name}"
        )
    from application.repositories.database.bind import db_manager

    logger.debug("<Application startup>")
    await db_manager.connect()
    logger.debug("<Application db-connected>")
