import asyncio
import json
import websockets
'''
web socket client 
'''
async def receive_messages(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            # 如果需要处理接收到的 JSON 数据，可以取消下一行的注释
            # data = json.loads(message)
            # print(f"Received data: {data}")

# WebSocket 服务器的地址
SERVER_URI = "ws://localhost:8001"

# 运行客户端
if __name__ == "__main__":
    asyncio.run(receive_messages(SERVER_URI))
