from fastapi import FastAPI
from db import create_db_and_tables
from routes import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["https://yourdomain.com"] in production
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)

# @app.on_event("startup")
# def startup():
#     create_db_and_tables()

@app.get("/")
def root():
    return {"status": "Backend is running!"}
