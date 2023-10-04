import asyncio
import websockets
import os
from videoFrames import videoFrames
import pause
import datetime

CLIENTS = set()

async def handler(websocket):
    print('Client connected')
    CLIENTS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CLIENTS.remove(websocket)
        print('Client disconnected')

async def broadcast(message):
    for websocket in CLIENTS.copy():
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            pass

async def broadcast_messages():
    for vid in os.listdir('./videos'):
        timer = datetime.datetime.now()
        for frame in videoFrames(f'./videos/{vid}'):
            await asyncio.sleep(0)
            message = frame.decode()
            await broadcast(message)
            pause.until(timer)
            timer = timer + datetime.timedelta(milliseconds=1000/25)


async def main():
    print('Listening')
    async with websockets.serve(handler, "localhost", 8000):
        await broadcast_messages()  # runs forever

if __name__ == "__main__":
    asyncio.run(main())