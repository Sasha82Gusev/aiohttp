import sys
import asyncio
import aiopg

from aiohttp import web
from app import MainPage, db
from app.views import AdvertisementView

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


DB_DSN = "postgres://postgres:41321122@127.0.0.1:5432/aiohttp_hw"


async def register_pg_pool(app):
    print(f"start")
    async with aiopg.pool.create_pool(DB_DSN) as pool:
        app['pg_pool'] = pool
        yield
        pool.close()
    print("end")


async def register_orm(app):
    await db.set_bind(DB_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/", MainPage)
    ])

    app.add_routes([
        web.get("/advertisement/{advert_id:\d+}", AdvertisementView),
        web.post("/advertisement", AdvertisementView),
        web.patch("/advertisement/{advert_id:\d+}", AdvertisementView),
        web.delete("/advertisement/{advert_id:\d+}", AdvertisementView)
    ])
    app.cleanup_ctx.append(register_pg_pool)
    app.cleanup_ctx.append(register_orm)
    web.run_app(app)