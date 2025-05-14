from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import user_controller, auth_controller, case_controller

app = FastAPI(title="GuardTree API", version="1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(case_controller.router)

@app.get("/")
async def root():
    return {"message": "Welcome to GuardTree API"}