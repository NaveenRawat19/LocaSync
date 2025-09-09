import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
from datetime import datetime

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # Dict of rooms to list of active websocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.max_connections_per_room = 10

    async def connect(self, websocket: WebSocket, room: str):
        if room not in self.active_connections:
            self.active_connections[room] = []
        if len(self.active_connections[room]) >= self.max_connections_per_room:
            await websocket.close(code=1001)  # Reject if room is full
            return False
        await websocket.accept()
        self.active_connections[room].append(websocket)
        return True

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections and websocket in self.active_connections[room]:
            self.active_connections[room].remove(websocket)
            if len(self.active_connections[room]) == 0:
                del self.active_connections[room]

    async def broadcast(self, room: str, message: str):
        if room not in self.active_connections:
            return
        to_remove = []
        for connection in self.active_connections[room]:
            try:
                await connection.send_text(message)
            except Exception:
                to_remove.append(connection)
        for conn in to_remove:
            self.disconnect(conn, room)

manager = ConnectionManager()

@app.websocket("/ws/chat/{room}/{username}")
async def websocket_endpoint(websocket: WebSocket, room: str, username: str):
    connection_accepted = await manager.connect(websocket, room)
    if not connection_accepted:
        return
    try:
        join_msg = json.dumps({
            "user": "system",
            "room": room,
            "message": f"{username} joined the chat",
            "timestamp": datetime.utcnow().isoformat()
        })
        await manager.broadcast(room, join_msg)

        while True:
            data = await websocket.receive_text()
            message_data = {
                "user": username,
                "room": room,
                "message": data,
                "timestamp": datetime.utcnow().isoformat()
            }
            await manager.broadcast(room, json.dumps(message_data))

    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        leave_msg = json.dumps({
            "user": "system",
            "room": room,
            "message": f"{username} left the chat",
            "timestamp": datetime.utcnow().isoformat()
        })
        await manager.broadcast(room, leave_msg)
    except Exception:
        manager.disconnect(websocket, room)
