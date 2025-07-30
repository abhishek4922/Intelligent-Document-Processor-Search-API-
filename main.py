from fastapi import FastAPI
from router.router import router  # relative import based on your structure
import uvicorn

app = FastAPI()

app.include_router(router, prefix="/api", tags=["Document Processing"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)