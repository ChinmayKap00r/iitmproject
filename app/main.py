from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.tasks import execute_task, read_file
from app.config import DATA_DIR  # Ensure DATA_DIR is correctly imported
import os

app = FastAPI(title="LLM Automation Agent")

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

@app.get("/run")
async def run_task(task: str):
    """Executes a task based on natural language input."""
    try:
        result = execute_task(task)
        return {"status": "success", "output": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_task_file(path: str):
    """Reads a file and returns its content."""
     # Normalize the path to avoid security issues (e.g., directory traversal attacks)
    normalized_path = os.path.abspath(os.path.join(DATA_DIR, os.path.relpath(path, "/data/")))

    try:
        content = read_file(normalized_path)
        return {"content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

# to run: python3 -m uvicorn main:app --reload