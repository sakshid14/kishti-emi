from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import psycopg2
import asyncio
import threading
from contextlib import asynccontextmanager

clients: list[WebSocket] = []
transaction_queue = asyncio.Queue()

def listen_to_transactions():
    DATABASE_URL = "postgresql://reconrebels_1:Loknath%404044@recons.postgres.database.azure.com/postgres"
    conn = psycopg2.connect(
        database="postgres",
        user="reconrebels_1",
        password="Loknath@4044",
        host="recons.postgres.database.azure.com",
        port=5432,
        sslmode="require"
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("LISTEN new_transaction;")
    print("🟢 Listening to 'new_transaction'...")

    while True:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            payload = notify.payload
            asyncio.run_coroutine_threadsafe(
                transaction_queue.put(payload), asyncio.get_event_loop()
            )

@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=listen_to_transactions, daemon=True).start()

    async def broadcast():
        while True:
            payload = await transaction_queue.get()
            disconnected = []
            for ws in clients:
                try:
                    await ws.send_text(payload)
                except Exception as e:
                    print("Error sending to client:", e)
                    disconnected.append(ws)
            for ws in disconnected:
                if ws in clients:
                    clients.remove(ws)

    asyncio.create_task(broadcast())

    yield

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print(f"Client connected. Total: {len(clients)}")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client disconnected")
        if websocket in clients:
            clients.remove(websocket)
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             print(f"Received from client: {data}")
#             await websocket.send_text(f"Server echo: {data}")
#     except WebSocketDisconnect:
#         print("Client disconnected")