from fastapi import FastAPI

app = FastAPI(
    title="Spy Cat Agency API",
    description="Backend API for managing spy cats, missions and targets",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
