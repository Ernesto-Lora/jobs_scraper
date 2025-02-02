from fastapi import FastAPI
from .database import engine, Base
from .routers import jobs

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(jobs.router)

@app.get("/")
def read_root():
    return {"status": "OK"}