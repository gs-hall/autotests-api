import asyncio

import websockets


async def main():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Привет, сервер!")

        for _ in range(5):
            message = await websocket.recv()
            print(message)


if __name__ == "__main__":
    asyncio.run(main())
