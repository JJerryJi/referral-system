from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uuid
import redis
from datetime import datetime
import asyncio
import threading 

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

connectionManager: {int:WebSocket}= {}

# WebSocket route to establish a connection
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    connectionManager[user_id] = websocket
    print('a new socket is connected')
    
    # async def send_notifications():
    print('start')
    while True:
        print('before')
        msg = await get_data()
        print('after')

        # print(int(msg))
        if msg is not None:
            notification = {
                "id": str(uuid.uuid4()),
                "title": 'Status Update of your application',
                "description": 'Please view it in your application!',
                "avatar": None,
                "type": 'mail',
                "createdAt": str(datetime.now()),
                "isUnRead": True,
                "filteredId": int(msg)
            }
        #     print('before send text')
            try:
                # await websocket.send_text('hello world')
                for websocket in connectionManager.values():
                    await websocket.send_json(notification)
            except WebSocketDisconnect:
                del connectionManager[user_id]
                print('socket disconnected')
                break
            except Exception as e:
                print('e', str(e))

    # Create a new thread to send notifications for this WebSocket connection
    # t = threading.Thread(target=lambda: asyncio.run(send_notifications()))
    # t.start()


    