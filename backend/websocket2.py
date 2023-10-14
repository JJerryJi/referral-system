from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uuid
import redis
from datetime import datetime
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

# This list will be used to store WebSocket instances for each user_id
connectionManager = {}

def get_data():
    while True:
        # for connected in connectionManager
        pass 

def get_data_and_send_notifications(user_id):
    while True:
        msg = redis_client.lpop('ws')
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
            try:
                for websocket in connectionManager.get(user_id, []):
                    websocket.send_json(notification)
            except WebSocketDisconnect:
                # Handle disconnections or errors here
                pass

# WebSocket route to establish a connection
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    if user_id not in connectionManager:
        connectionManager[user_id] = []
    connectionManager[user_id].append(websocket)

    # Start a thread for this user's notifications
    thread = threading.Thread(target=get_data_and_send_notifications, args=(user_id,))
    thread.daemon = True
    thread.start()

    try:
        while True:
            # You can add additional logic here if needed
            pass
    except WebSocketDisconnect:
        connectionManager[user_id].remove(websocket)
