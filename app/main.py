from fastapi import FastAPI

from app.health.router import router as health_router

app = FastAPI(
    title="Net Incident Tracker",
    description="API for tracking and grouping network incidents",
    version="0.1.0",
)

app.include_router(health_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Net Incident Tracker API"}