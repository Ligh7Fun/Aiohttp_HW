import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from models import Ads, Session


def get_http_error(error_class, message: str):
    return error_class(
        text=json.dumps({"error": message}),
        content_type="application/json",
    )


async def get_ads_by_id(session: Session, ads_id: int):
    ads = await session.get(Ads, ads_id)
    if ads is None:
        raise get_http_error(web.HTTPNotFound, f"Ads with id {ads_id} not found")
    return ads


async def add_ads(session: Session, ads: Ads):
    try:
        session.add(ads)
        await session.commit()
    except IntegrityError:
        raise get_http_error(web.HTTPConflict, f"Ads with id {ads.id} already exists")
    return ads
