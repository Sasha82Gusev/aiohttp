from datetime import datetime
from asyncpg import UniqueViolationError
from gino import Gino
from aiohttp import web

db = Gino()

class BaseModelMixin:

    @classmethod
    async def by_id(cls, obj_id):
        obj = await cls.get(obj_id)
        if obj:
            return obj
        else:
            raise web.HTTPNotFound()

    @classmethod
    async def create_model(cls, **kwargs):
        try:
            obj = await cls.create(**kwargs)
            return obj

        except UniqueViolationError:
            raise web.HTTPBadRequest()

    @classmethod
    async def update_model(cls, obj_id, **kwargs):
        get = await cls.by_id(obj_id)
        await get.update(**kwargs).apply()
        response = await cls.by_id(obj_id)
        return response



class Advertisements(db.Model, BaseModelMixin):

    __tablename__ = "Advertisements"

    id = db.Column(db.Integer(), primary_key=True)
    header = db.Column(db.String(50))
    text = db.Column(db.String(1000))
    created_date = db.Column(db.DateTime, default=datetime.today)
    owner_id = db.Column(db.String(50))

    def to_dict(self):
        Advertisements = {
            "id": self.id,
            "header": self.header,
            "text": self.text,
            "created_date": str(self.created_date),
            "owner_id": self.owner_id
        }
        return Advertisements
