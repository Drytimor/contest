from fastapi import APIRouter
from .dependencies.auth import CurrentUserDepends
from .routes.participants import participant_router, qualifying_router
from .routes.auth import auth_router, user_router
from .routes.competitions import (
    competition_router, contribution_router, complex_router, result_router
)

api_router = APIRouter()

api_router.include_router(auth_router)

api_router.include_router(
    user_router,
    dependencies=[CurrentUserDepends]
)
api_router.include_router(
    competition_router,
    dependencies=[CurrentUserDepends]
)
api_router.include_router(
    contribution_router,
    dependencies=[CurrentUserDepends]
)
api_router.include_router(
    complex_router,
    dependencies=[CurrentUserDepends]
)
api_router.include_router(
    participant_router,
    dependencies=[CurrentUserDepends]
)
api_router.include_router(
    qualifying_router,
    dependencies=[CurrentUserDepends]
)
api_router.include_router(
    result_router,
    dependencies=[CurrentUserDepends]
)