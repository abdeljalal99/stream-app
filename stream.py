import asyncio
import websockets
import os
from stream_helpers.video_frames import video_frames, get_framerate
from stream_helpers.audio_fragments import init_audio, next_audio_fragment
import pause
import datetime
import json


CLIENTS = set()
FRAMERATE = 0
PACKAGE_SIZE = 1


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
        video_path = f'./videos/{vid}'
        FRAMERATE = int(get_framerate(video_path))
        print('Framerate:', FRAMERATE)
        timer = datetime.datetime.now()
        audio = init_audio(video_path)
        current_second = 1
        frames = []

        for frame in video_frames(video_path):
            await asyncio.sleep(0)
            message = frame.decode()
            frames.append(message)

            if len(frames) == PACKAGE_SIZE * FRAMERATE:
                audio_fragment = next_audio_fragment(audio, current_second*PACKAGE_SIZE*1000)
                data = { "frames": frames, "audio": audio_fragment }
                await broadcast(json.dumps(data))
                frames = []
                current_second += PACKAGE_SIZE

            pause.until(timer)
            timer = timer + datetime.timedelta(milliseconds=1000/FRAMERATE)


async def main():
    print('Listening')
    async with websockets.serve(handler, "localhost", 8000):
        await broadcast_messages()

if __name__ == "__main__":
    asyncio.run(main())
