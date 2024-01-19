from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from routes import tasks, auth, users
from db import Base, engine
from decouple import config

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(users.router)

FRONTEND_URL = config('FRONTEND_URL')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["home"])
async def root():
    return RedirectResponse(url="/docs")
