import asyncio
import time
import threading
from fastapi import FastAPI


app = FastAPI()


@app.get('/sync/{id}')
def sync_func(id: int):
    start = time.perf_counter()
    print(f'Количество потоков: {threading.active_count()}')
    print(f'Начал выполнение sync {id}: {time.time():.2f}')
    time.sleep(3)
    print(f'Закончил выполнение sync {id}: {time.time():.2f}')


@app.get('/async/{id}')
async def async_func(id: int):
    start = time.perf_counter()
    print(f'Количество потоков: {threading.active_count()}')
    print(f'Начал выполнение async {id}: {time.time():.2f}')
    await asyncio.sleep(3)
    print(f'Закончил выполнение async {id}: {time.time():.2f}')
    print(f'Время выполнения: {time.perf_counter() - start}')