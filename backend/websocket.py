from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uuid
import redis
from datetime import datetime
import asyncio
import threading 
import time 

app = FastAPI()

# Allow WebSocket connections from the React frontend's domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "ws://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

async def get_data():
    msg = redis_client.lpop('ws')
    # return msg 
    while not msg:
        msg = redis_client.lpop('ws')
        await asyncio.sleep(1)
    return msg

async def task_with_delay(thread_name, delay):
    print(f"Thread {thread_name} is starting.")
    while True:
        key, msg = redis_client.blpop('ws')
        if msg:
            print('length: ', len(connectionManager))
            for connected in connectionManager.values():
                notification = {
                    "id": str(uuid.uuid4()),
                    "title": 'Status Update of your application',
                    "description": 'Please view it in your application!',
                    "avatar": None,
                    "type": 'mail',
                    "createdAt": str(datetime.now().isoformat()),
                    "isUnRead": True,
                    "filteredId": int(msg)
                }
                await connected.send_json(notification)
            print('send message to all!')

# Create multiple threads
thread1 = threading.Thread(target=lambda: asyncio.run(task_with_delay("Thread 1", 2)))
thread1.daemon = True 

# Start the threads
thread1.start()

connectionManager: {int:WebSocket}= {}

# WebSocket route to establish a connection
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    connectionManager[user_id] = websocket
    print('a new socket is connected')
    
    # async def send_notifications():
    print('start')
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        del connectionManager[user_id]
        print(f'deleted: {user_id}')
    except Exception as e:
        print('e', str(e))


    