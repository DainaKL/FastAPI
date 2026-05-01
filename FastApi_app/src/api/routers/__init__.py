from src.api.routers.category import router as category_router
from src.api.routers.comments import router as comments_router
from src.api.routers.location import router as location_router
from src.api.routers.posts import router as posts_router
from src.api.routers.users import router as users_router
from src.api.routers.auth import router as auth_router

__all__ = [
    "category_router",
    "comments_router",
    "location_router",
    "posts_router",
    "users_router",
    "auth_router",
]
