import asyncio
import websockets

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
    i = 0
    m = [1, 2, 3, 4, 5]
    while True:
        await asyncio.sleep(0.1)
        message = f'{m[i]}'
        await broadcast(message)
        i = 0 if i >= len(m)-1 else i+1

async def main():
    print('Listening')
    async with websockets.serve(handler, "localhost", 8000):
        await broadcast_messages()  # runs forever

if __name__ == "__main__":
    asyncio.run(main())