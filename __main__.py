import uvicorn

import config

uvicorn_logging_config = uvicorn.config.LOGGING_CONFIG
uvicorn_logging_config["formatters"]["access"][
    "fmt"
] = "[%(asctime)s][%(levelname)s] %(message)s"
uvicorn_logging_config["formatters"]["default"][
    "fmt"
] = "[%(asctime)s][%(levelname)s] %(message)s"

if __name__ == "__main__":
    uvicorn.run(
        "api:server",
        host=config.HOST,
        port=config.PORT,
        log_config=uvicorn_logging_config,
        use_colors=True,
        log_level=config.LOG_LEVEL.lower(),
        reload=config.DEBUG,
        workers=1,
    )
