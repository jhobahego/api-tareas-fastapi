from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from routes import tasks
from db import Base, engine
from decouple import config

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(tasks.router)

FRONTEND_URL = config('FRONTEND_URL')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
