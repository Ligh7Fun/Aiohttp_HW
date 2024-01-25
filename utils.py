import json
import re

import bcrypt
from aiohttp import web
from sqlalchemy.exc import IntegrityError

from models import Session, User


def get_http_error(error_class, message: str):
    return error_class(
        text=json.dumps({"error": message}),
        content_type="application/json",
    )


async def get_user_by_id(session: Session, user_id: int):
    user = await session.get(User, user_id)
    if user is None:
        raise get_http_error(web.HTTPNotFound, f"User with id {user_id} not found")
    return user


async def add_user(session: Session, user: User):
    try:
        session.add(user)
        await session.commit()
    except IntegrityError:
        raise get_http_error(
            web.HTTPConflict, f"User with name {user.name} already exists"
        )
    return user


async def hash_password(password: str):
    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode()
    return password


def check_password(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)
