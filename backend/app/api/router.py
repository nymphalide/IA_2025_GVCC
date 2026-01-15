from fastapi import APIRouter

from app.api.minmax.routes import router as minmax_router
from app.api.nash.routes import router as nash_router
from app.api.strategy.routes import router as strategy_router
from app.api.rl.routes import router as rl_router
from app.api.csp.routes import router as csp_router
from app.api.bayes.routes import router as bayes_router
from app.api.test.routes import router as test_router

router = APIRouter()

router.include_router(minmax_router)
router.include_router(nash_router)
router.include_router(strategy_router)
router.include_router(bayes_router, prefix="/bayes", tags=["Bayesian Networks"])
router.include_router(rl_router)
router.include_router(csp_router)
router.include_router(test_router)
