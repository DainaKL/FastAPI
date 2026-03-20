from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routers import posts_router, category_router, location_router, comments_router, users_router


def create_app() -> FastAPI:
    app = FastAPI() 
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(posts_router)
    app.include_router(category_router)
    app.include_router(location_router)
    app.include_router(comments_router)
    app.include_router(users_router)
    return app
