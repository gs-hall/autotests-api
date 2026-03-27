import asyncio

import websockets


async def handle_connection(websocket):
	async for message in websocket:
		print(f"Получено сообщение от пользователя: {message}")

		for i in range(1, 6):
			await websocket.send(f"{i} Сообщение пользователя: {message}")


async def main():
	async with websockets.serve(handle_connection, "localhost", 8765):
		print("WebSocket сервер запущен на ws://localhost:8765")
		await asyncio.Future()


if __name__ == "__main__":
	asyncio.run(main())
