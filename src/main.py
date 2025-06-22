from contextlib import asynccontextmanager
import logging
import sys
import uvicorn

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))  # noqa: E402

from src.init import redis_manager

from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.images import router as router_image
from src.api.facilities import router as router_facilities

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)
app.include_router(router_image)


@app.get("/")
def root():
    return "Привет"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
