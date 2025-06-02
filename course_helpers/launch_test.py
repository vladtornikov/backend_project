# import asyncio
# import aiohttp
#
#
# async def get_data(i: int, endpoint: str):
#     print(f'Начал выполнение: {i}')
#     url = f'http://127.0.0.1:25567/{endpoint}/{i}'
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             print(f'Закончил выполнение: {i}')
#
# async def launch():
#     await asyncio.gather(
#         *[get_data(i, 'async') for i in range(500)]
#     )
#
# asyncio.run(launch())
