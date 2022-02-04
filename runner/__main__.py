import os

from runner.utils.logs_config import SETTINGS_LOGGER

if __name__ == "__main__":
    import uvicorn

    is_debug = os.getenv("DEBUG") == "True"

    uvicorn.run(
        "runner.run:application",
        host="0.0.0.0",
        port=5001,
        debug=is_debug,
        access_log=True,
        log_config=SETTINGS_LOGGER,
        reload=is_debug,
    )
