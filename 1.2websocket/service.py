import json
import asyncio
import redis
import websockets
‘’‘
通过把数据加到redis 中 使用websocket通知给客户端 
’‘’
# 连接到 Redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

# 用于存储连接的客户端
connected_clients = set()

async def read_from_redis_and_broadcast():
    while True:
        # 从 Redis 列表中读取数据
        list_key = 'my_list'
        #data = r.lrange(list_key, 0, -1)  # 获取列表中的所有元素
        data = r.lpop(list_key)
        if data != None:
          message = json.dumps({"data": str(data)})  # 将数据转换为 JSON 格式
          # 向所有连接的客户端广播消息
          #message = "test"
          await broadcast(message)
          # 等待一段时间后再次读取
          await asyncio.sleep(0.5)  # 每5秒发送一次

async def broadcast(message):
    # 向所有连接的客户端发送消息
    for client in connected_clients:
        await client.send(message)

async def handler(websocket, path):
    # 每当有新客户端连接时，将其添加到客户端集合中
    connected_clients.add(websocket)
    try:
        # 运行一个循环来接收客户端的消息
        async for message in websocket:
            print(f"Received message from client: {message}")
    finally:
        # 客户端断开连接时，从集合中移除
        connected_clients.remove(websocket)

# 启动 WebSocket 服务器
async def start_server():
    async with websockets.serve(handler, "localhost", 8001):
        # 启动广播任务
        await read_from_redis_and_broadcast()
        await asyncio.Future()  # 运行直到被取消

# 运行服务器
if __name__ == "__main__":
    asyncio.run(start_server())
