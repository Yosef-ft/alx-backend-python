import aiosqlite
import asyncio


async def async_fetch_users():
    async with aiosqlite.connect('./../python-decorators-0x01/users.db') as db:

        async with db.execute("SELECT * FROM users") as cursor:
            async for row in cursor:
                print(row)


async def async_fetch_older_users():
    async with aiosqlite.connect('./../python-decorators-0x01/users.db') as db:

        async with db.execute("SELECT * FROM users where age > 40") as cursor:
            async for row in cursor:
                print(row)



async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )



asyncio.run(fetch_concurrently())    