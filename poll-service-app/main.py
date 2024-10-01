from contextlib import asynccontextmanager

import uvicorn
from core.models import db_helper
from fastapi import FastAPI

from core.config import settings
from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(
    api_router,
    prefix='/api',
)

if __name__ == '__main__':
    uvicorn.run(
        'main:main_app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
