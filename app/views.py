from aiohttp import web
from app.models import Advertisements


class MainPage(web.View):

    async def get(self):
        return web.json_response({"status": "OK"})



class AdvertisementView(web.View):

    async def get(self):
        advert = int(self.request.match_info["advert_id"])
        get_advert = await Advertisements.by_id(advert)
        return web.json_response(get_advert.to_dict())

    async def post(self):
        data = await self.request.json()
        if bool("header" and "text" and "owner_id" not in data.keys()):
            raise web.HTTPBadRequest()
        create = await Advertisements.create_model(**data)
        return web.json_response(create.to_dict())

    async def patch(self):
        data = await self.request.json()
        advert = int(self.request.match_info["advert_id"])
        updated_data = await Advertisements.update_model(advert, **data)
        return web.json_response(updated_data.to_dict())

    async def delete(self):
        advert = int(self.request.match_info["advert_id"])
        get_advert = await Advertisements.by_id(advert)
        if not get_advert:
            return web.HTTPNotFound()
        await get_advert.delete()
        return web.HTTPNoContent()
