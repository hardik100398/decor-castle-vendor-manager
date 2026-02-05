from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.vendors_router import router as vendors_router


# Load environment variables from a .env file if present
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Decor Castle Vendor Manager API")
APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(title=APP_NAME)
app.include_router(vendors_router)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.get("/")
async def root() -> dict:
    return {
        "message": f"Welcome to {APP_NAME}",
        "environment": APP_ENV,
    }



