from aiogram import Router


def setup_routers() -> Router:
    from . import (
    start,
    registration,
    view_profiles,
    my_profile,
    reference,
    )
    router = Router()
    router.include_router(start.router)
    router.include_router(registration.router)
    router.include_router(view_profiles.router)
    router.include_router(my_profile.router)
    router.include_router(reference.router)
    return router
