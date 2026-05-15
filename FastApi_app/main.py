import asyncio
import uvicorn

from src.app import create_app
from src.core.logger import logger

app = create_app()


async def run() -> None:
    config = uvicorn.Config("main:app", host="127.0.0.1", port=8000, reload=False)
    server = uvicorn.Server(config=config)
    logger.info("Starting FastAPI application on http://127.0.0.1:8000")
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("Сервер был остановлен вручную")
        print("\nСервер был остановлен вручную")
