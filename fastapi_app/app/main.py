from fastapi import FastAPI
import os

# Get the current working directory
current_directory = os.getcwd()

# Print the current directory
print(current_directory)


# Alternative using pathlib (more modern and often preferred):
from pathlib import Path

current_directory_pathlib = Path.cwd()
print(current_directory_pathlib)

# Or, if you want a string representation specifically:
print(str(Path.cwd()))

from .routers import jobs
app = FastAPI()
app.include_router(jobs.router)

@app.get("/")
def read_root():
    return {"status": "OK"}