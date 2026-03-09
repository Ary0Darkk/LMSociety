from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import random

app = FastAPI()

# Enable CORS for React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class SocietyManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        # Initial Society Members
        self.agents = [
            {"id": "1", "name": "Philosopher", "status": "idle"},
            {"id": "2", "name": "Scientist", "status": "idle"},
            {"id": "3", "name": "Economist", "status": "idle"}
        ]

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

manager = SocietyManager()

@app.websocket("/ws/society")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send initial agent list
        await websocket.send_json({"type": "INIT_SOCIETY", "data": manager.agents})
        
        while True:
            # Simulate a debate loop
            for agent in manager.agents:
                # 1. Set agent to 'thinking'
                agent["status"] = "thinking"
                await manager.broadcast({"type": "UPDATE_STATUS", "id": agent["id"], "status": "thinking"})
                
                await asyncio.sleep(random.uniform(1, 3)) # Simulate LLM delay
                
                # 2. Agent speaks
                message = f"I believe we should consider the {agent['name']} perspective on this matter..."
                agent["status"] = "idle"
                await manager.broadcast({
                    "type": "NEW_MESSAGE", 
                    "id": agent["id"], 
                    "text": message,
                    "status": "idle"
                })
                
                await asyncio.sleep(1)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)