"""
API路由包
"""
from .astro_routes import router as astro_router
from .test_routes import router as test_router
from .root_routes import router as root_router
from .calendar_routes import router as calendar_router

__all__ = [
    'astro_router',
    'test_router',
    'root_router',
    'calendar_router'
] 