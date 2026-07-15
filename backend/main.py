"""
main.py — Fin101 FastAPI Uygulaması

Endpoint'ler:
  GET  /          → Sağlık kontrolü
  POST /users/    → Kullanıcı kaydı
  POST /chat/     → Sohbet (hafızalı, RAG destekli)
"""

from contextlib import asynccontextmanager
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorDatabase

import database as db_ops
from database import connect_db, close_db, get_database
from rag import ask_mentor
from models import (
    ChatMessage,
    ChatResponse,
    ConversationCreate,
    MessageCreate,
    UserCreate,
    UserResponse,
)


# ---------------------------------------------------------------------------
# Uygulama Yaşam Döngüsü
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


# ---------------------------------------------------------------------------
# FastAPI Uygulaması
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Fin101 API",
    description="Finansal okuryazarlık ve yapay zeka mentorluk platformu backend'i.",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Dependency Injection — Veritabanı
# ---------------------------------------------------------------------------

def get_db() -> AsyncIOMotorDatabase:
    return get_database()


DatabaseDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]


# ===========================================================================
# ENDPOINT'LER
# ===========================================================================


@app.get("/", tags=["Sistem"])
async def root():
    """Sağlık kontrolü — API'nin ayakta olduğunu doğrular."""
    return {"status": "ok", "message": "Fin101 API is running.", "version": "0.3.0"}


# ---------------------------------------------------------------------------
# POST /users/ — Kullanıcı Kaydı
# ---------------------------------------------------------------------------

@app.post(
    "/users/",
    response_model=UserResponse,
    status_code=201,
    tags=["Kullanıcılar"],
    summary="Yeni kullanıcı oluştur",
)
async def create_user_endpoint(user: UserCreate, db: DatabaseDep):
    """
    Yeni bir kullanıcı kaydeder.

    - **name**: Kullanıcı adı soyadı
    - **email**: Benzersiz e-posta adresi (duplicate → 400)
    - **risk_profile**: Düşük / Orta / Yüksek (varsayılan: Orta)
    - **virtual_balance**: Başlangıç sanal bakiye (varsayılan: 10000.0)
    """
    try:
        inserted_id = await db_ops.create_user(db, user)
    except ValueError as exc:
        # create_user duplicate e-posta için ValueError fırlatır
        raise HTTPException(status_code=400, detail=str(exc))

    # Kaydedilen belgeyi geri çekip UserResponse ile döndür
    created_doc = await db_ops.get_user_by_id(db, inserted_id)
    if not created_doc:
        raise HTTPException(status_code=500, detail="Kullanıcı kaydedildi fakat geri okunamadı.")

    return UserResponse(**created_doc)


# ---------------------------------------------------------------------------
# POST /chat/ — Sohbet ve Hafıza Akışı
# ---------------------------------------------------------------------------

@app.post(
    "/chat/",
    response_model=ChatResponse,
    tags=["Sohbet"],
    summary="Sokratik Mentor'a mesaj gönder (hafızalı)",
)
async def chat_endpoint(request: MessageCreate, db: DatabaseDep):
    """
    Hafızalı, RAG destekli sohbet endpoint'i.

    **Akış:**
    1. `session_id` yoksa yeni `Conversation` belgesi oluşturulur.
    2. Kullanıcı mesajı `messages` koleksiyonuna kaydedilir.
    3. Oturumdaki son 10 mesaj geçmiş olarak çekilir.
    4. Geçmiş + RAG bağlamı Gemini'ye gönderilir, gerçek yanıt alınır.
    5. Asistan yanıtı `messages` koleksiyonuna kaydedilir.
    6. `reply` ve `session_id` döndürülür.
    """

    # ------------------------------------------------------------------
    # 1. Oturum Yönetimi: session_id yoksa yeni conversation oluştur
    # ------------------------------------------------------------------
    session_id: UUID

    if request.session_id is None:
        # Yeni oturum: başlık olarak kullanıcı mesajının ilk 60 karakteri
        title = request.message[:60] + ("..." if len(request.message) > 60 else "")
        new_conv = ConversationCreate(
            user_id=request.user_id,
            title=title,
        )
        conversation_id = await db_ops.create_conversation(db, new_conv)
        session_id = new_conv.session_id        # uuid4 ile üretildi
    else:
        # Mevcut oturumu bul
        session_id = request.session_id
        existing_conv = await db_ops.get_conversation_by_session(db, session_id)

        if not existing_conv:
            raise HTTPException(
                status_code=404,
                detail=f"session_id '{session_id}' bulunamadı. Yeni oturum için session_id göndermeden tekrar deneyin.",
            )
        conversation_id = existing_conv["id"]

    user_msg = ChatMessage(role="user", content=request.message)
    await db_ops.save_message(db, conversation_id, session_id, request.user_id, user_msg)

    history = await db_ops.get_conversation_history(db, session_id, limit=10)

    real_reply = await ask_mentor(request.message, history)

    assistant_msg = ChatMessage(role="assistant", content=real_reply)
    await db_ops.save_message(db, conversation_id, session_id, request.user_id, assistant_msg)

    return ChatResponse(reply=real_reply, session_id=session_id)
