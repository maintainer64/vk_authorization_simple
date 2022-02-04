from typing import Dict, Any

from fastapi_jsonrpc import API
from starlette.templating import Jinja2Templates

from runner.configs import config

app_config: Dict[str, Any] = (
    dict(debug=True)
    if config.environment.LOCAL == config.environment
    else dict(docs_url=None, redoc_url=None, openapi_url=None, debug=False)
)

app = API(**app_config)

templates = Jinja2Templates(directory="/opt/app/runner/static" if config.is_docker else "static")
