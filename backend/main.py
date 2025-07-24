from fastapi import FastAPI
from db import create_db_and_tables
from routes import router

app = FastAPI()
app.include_router(router)

# @app.on_event("startup")
# def startup():
#     create_db_and_tables()

@app.get("/")
def root():
    return {"status": "Backend is running!"}
