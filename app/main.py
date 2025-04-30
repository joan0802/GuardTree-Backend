from fastapi import FastAPI

app = FastAPI(title="GuardTree API", version="1.0")

@app.get("/")
async def root():
    return {"message": "Welcome to GuardTree API"}