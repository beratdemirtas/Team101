from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from database import connect_db, close_db, get_database
from models import UserCreate
from rag import ask_mentor
from api import market, news


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


@app.get("/market/history/{ticker}")
async def stock_history(ticker: str, start: str, end: str):
    # yfinance senkron çalışır; event loop'u kilitlememesi için threadpool'a atılır.
    data = await run_in_threadpool(market.get_stock_history, ticker, start, end)
    return {"ticker": ticker, "data": data}


@app.get("/market/price/{ticker}")
async def stock_price(ticker: str):
    price = await run_in_threadpool(market.get_current_price, ticker)
    return price


@app.get("/news/company/{symbol}")
async def company_news(symbol: str, from_date: str, to_date: str):
    # finnhub-python da senkron; aynı sebeple threadpool'a atılır.
    articles = await run_in_threadpool(news.get_company_news, symbol, from_date, to_date)
    return {"symbol": symbol, "articles": articles}


@app.get("/news/market")
async def market_news(category: str = "general"):
    articles = await run_in_threadpool(news.get_market_news, category)
    return {"category": category, "articles": articles}
