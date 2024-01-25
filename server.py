from aiohttp import web

from models import Session, User, engine, init_orm
from utils import add_user, get_user_by_id

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


class UserView(web.View):
    @property
    def session(self) -> Session:
        return self.request.session

    @property
    def user_id(self):
        return int(self.request.match_info.get("user_id"))

    async def get_user(self):
        return await get_user_by_id(self.session, self.user_id)

    async def get(self) -> None:
        user = await self.get_user()
        return web.json_response(user.dict)

    async def post(self) -> None:
        json_data = await self.request.json()
        user = User(**json_data)
        await add_user(self.session, user)
        return web.json_response({"id": user.id})

    async def patch(self) -> None:
        json_data = await self.request.json()
        user = await self.get_user()
        for field, value in json_data.items():
            setattr(user, field, value)
        await add_user(self.session, user)
        return web.json_response(user.dict)

    async def delete(self) -> None:
        user = await self.get_user()
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.get("/user/{user_id:\d+}", UserView),
        web.patch("/user/{user_id:\d+}", UserView),
        web.delete("/user/{user_id:\d+}", UserView),
        web.post("/user", UserView),
    ]
)

if __name__ == "__main__":
    web.run_app(app, port=8080)
