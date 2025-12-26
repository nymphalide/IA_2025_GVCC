from fastapi import APIRouter

from app.api.minmax.routes import router as minmax_router
from app.api.nash.routes import router as nash_router
from app.api.strategy.routes import router as strategy_router
from app.api.csp.routes import router as csp_router

router = APIRouter()

router.include_router(minmax_router)
router.include_router(nash_router)
router.include_router(strategy_router)
router.include_router(csp_router) # Added