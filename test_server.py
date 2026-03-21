"""Quick test to verify static file serving"""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/dashboard.html")
async def dashboard():
    return FileResponse("frontend/dashboard.html")

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    print("Starting test server on http://127.0.0.1:8001")
    print("Try accessing:")
    print("  - http://127.0.0.1:8001/")
    print("  - http://127.0.0.1:8001/static/style.css")
    print("  - http://127.0.0.1:8001/dashboard.html")
    uvicorn.run(app, host="127.0.0.1", port=8001)
