from fastapi import FastAPI, WebSocket
import psycopg2
import threading

app = FastAPI()
clients = []

def listen_to_transactions():
    conn = psycopg2.connect(
        dbname="postgres",
        user="reconrebels_1",
        password="Loknath%404044",
        host="recons.postgres.database.azure.com"
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
            for ws in clients:
                try:
                    ws.send_text(payload)
                except Exception as e:
                    print("Error sending to WebSocket:", e)

threading.Thread(target=listen_to_transactions, daemon=True).start()

@app.websocket("/update-transaction")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)