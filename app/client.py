import asyncio
from aiohttp import ClientSession



async def get_advert(advert_id):
    async with ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8080/advertisement/{advert_id}") as resp:
            return await resp.text()


async def post_advert():
    async with ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/advertisement", json={
            "header": "zagolovok",
            "text": "text",
            "owner_id": "avtor"
        }) as resp:
            if resp.status != 201:
                return await resp.text()
            return await resp.json()


async def patch_adverts(owner_id, text, header, advert_id):
    async with ClientSession() as session:
        async with session.patch(f"http://127.0.0.1:8080/advertisement/{advert_id}", json={
            "header": header,
            "text": text,
            "owner_id": owner_id
        }) as resp:
            if resp.status != 200:
                return await resp.text()
            return await resp.json()


async def delete_advert(advert_id):
    async with ClientSession() as session:
        async with session.delete(f"http://127.0.0.1:8080/advertisement/{advert_id}") as resp:
            return {"status": resp.status}


async def main():
    response_get = await get_advert(2)
    print('GET--', response_get)
    response_post = await post_advert()
    print('POST--', response_post)
    response_patch = await patch_adverts("Sanya", "new_data", "new_zagolovok", 1)
    print('PATCH--', response_patch)
    response_del = await delete_advert(6)
    print('DEL--', response_del)


asyncio.run(main())
