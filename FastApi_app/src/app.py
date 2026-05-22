import time
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.routers import (
    category_router,
    comments_router,
    location_router,
    posts_router,
    users_router,
    auth_router,
)
from src.core.logger import logger


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Blog API",
        version="1.0.0",
        swagger_ui_parameters={
            "persistAuthorization": True,
            "displayRequestDuration": True,
        },
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {process_time:.3f}s"
        )
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(posts_router)
    app.include_router(category_router)
    app.include_router(location_router)
    app.include_router(comments_router)
    app.include_router(users_router)

    app.mount("/media", StaticFiles(directory="media"), name="media")

    return app
