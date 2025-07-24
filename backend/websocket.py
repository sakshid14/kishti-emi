from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import psycopg2
import asyncio
import threading
from contextlib import asynccontextmanager

clients: list[WebSocket] = []
transaction_queue = asyncio.Queue()

def listen_to_transactions(loop: asyncio.AbstractEventLoop):
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

            # Use thread-safe way to schedule coroutine on the main loop
            loop.call_soon_threadsafe(
                asyncio.create_task,
                transaction_queue.put(payload)
            )

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()

    # Start database listener in a separate thread
    listener_thread = threading.Thread(
        target=listen_to_transactions,
        args=(loop,),
        daemon=True
    )
    listener_thread.start()

    # Start the broadcast coroutine
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
    print(f"Client connected. Total clients: {len(clients)}")
    try:
        while True:
            await websocket.receive_text()  # Keeps the connection alive
    except WebSocketDisconnect:
        print("Client disconnected")
        if websocket in clients:
            clients.remove(websocket)
