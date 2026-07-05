from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from database import connect_db, close_db, get_database
from models import UserCreate
from rag import ask_mentor


class ChatRequest(BaseModel):
    message: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Fin101 API",
    description="Finansal okuryazarlık ve yapay zeka mentorluk platformu backend'i.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> AsyncIOMotorDatabase:
    return get_database()


DatabaseDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]


@app.get("/")
async def root():
    return {"status": "ok", "message": "Fin101 API is running."}


@app.post("/users/", status_code=201)
async def create_user(user: UserCreate, db: DatabaseDep):
    collection = db["Users"]

    existing = await collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=409, detail="Bu e-posta adresi zaten kayıtlı.")

    result = await collection.insert_one(user.model_dump())
    return {"id": str(result.inserted_id), "message": "Kullanıcı başarıyla oluşturuldu."}


@app.post("/chat/")
async def chat(request: ChatRequest):
    answer = await ask_mentor(request.message)
    return {"reply": answer}
