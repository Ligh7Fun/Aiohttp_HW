from aiohttp import web

from models import Ads, Session, engine, init_orm
from utils import add_ads, get_ads_by_id

app = web.Application()


async def init_db(app: web.Application):
    print("START")
    await init_orm()
    yield
    print("FINISH")
    await engine.dispose()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(init_db)
app.middlewares.append(session_middleware)


class AdsView(web.View):
    @property
    def session(self) -> Session:
        return self.request.session

    @property
    def ads_id(self):
        return int(self.request.match_info.get("ads_id"))

    async def get_ads(self):
        return await get_ads_by_id(self.session, self.ads_id)

    async def get(self) -> None:
        ads = await self.get_ads()
        return web.json_response(ads.dict)

    async def post(self) -> None:
        json_data = await self.request.json()
        ads = Ads(**json_data)
        await add_ads(self.session, ads)
        return web.json_response({"id": ads.id})

    async def patch(self) -> None:
        json_data = await self.request.json()
        ads = await self.get_ads()
        for field, value in json_data.items():
            setattr(ads, field, value)
        await add_ads(self.session, ads)
        return web.json_response(ads.dict)

    async def delete(self) -> None:
        ads = await self.get_ads()
        await self.session.delete(ads)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.get("/ads/{ads_id:\d+}", AdsView),
        web.patch("/ads/{ads_id:\d+}", AdsView),
        web.delete("/ads/{ads_id:\d+}", AdsView),
        web.post("/ads", AdsView),
    ]
)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
