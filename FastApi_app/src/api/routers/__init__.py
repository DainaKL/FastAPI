from src.api.routers.posts import router as posts_router
from src.api.routers.category import router as category_router
from src.api.routers.location import router as location_router 
from src.api.routers.comments import router as comments_router
from src.api.routers.users import router as users_router


__all_ = [
    "posts_router",
    "category_router",
    "location_router",
    "comments_router",
    "users_router"
]
