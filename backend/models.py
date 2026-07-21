from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Yardımcı: UTC şimdiki zamanı döndürür (default_factory için)
# ---------------------------------------------------------------------------
def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ===========================================================================
# KULLANICI MODELLERİ
# ===========================================================================

class UserCreate(BaseModel):
    """
    Yeni kullanıcı kaydı için istemciden gelen veri.
    POST /users/ endpoint'i bu modeli alır.
    """
    name: str
    email: EmailStr
    risk_profile: Literal["Düşük", "Orta", "Yüksek"] = "Orta"
    virtual_balance: float = Field(default=10000.0, ge=0)
    currency: Literal["TRY", "USD"] = "TRY"
    avatar_url: Optional[str] = None


class UserInDB(UserCreate):
    """
    MongoDB'deki tam kullanıcı belgesi.
    Kayıt sırasında eklenen alanları içerir; şifre alanı Sprint 3 (JWT) ile gelecek.
    """
    xp_score: int = Field(default=0, ge=0)
    level: int = Field(default=1, ge=1)
    badges: list[str] = Field(default_factory=list)
    is_active: bool = True
    created_at: datetime = Field(default_factory=_utcnow)
    last_active_at: datetime = Field(default_factory=_utcnow)


class UserResponse(BaseModel):
    """
    API yanıtı için kullanıcı özeti.
    Hassas alan içermez; ObjectId string olarak döner.
    """
    id: str
    name: str
    email: EmailStr
    risk_profile: str
    virtual_balance: float
    currency: str
    avatar_url: Optional[str]
    xp_score: int
    level: int
    badges: list[str]
    created_at: datetime


# ===========================================================================
# SOHBET & HAFIZA MODELLERİ
# ===========================================================================

class ChatMessage(BaseModel):
    """
    Tek bir mesajı temsil eder (user veya assistant).
    Frontend'in beklediği { role, content, timestamp } yapısıyla örtüşür;
    ancak timestamp DB'de ISO 8601 datetime olarak saklanır.
    """
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime = Field(default_factory=_utcnow)

    model_config = {
        "json_schema_extra": {
            "example": {
                "role": "user",
                "content": "Hisse senedi nedir?",
                "created_at": "2026-07-12T20:06:26Z",
            }
        }
    }


class ConversationCreate(BaseModel):
    """
    Yeni sohbet oturumu (session) başlatmak için kullanılan model.
    Frontend ilk mesajı gönderirken session_id yoksa backend bu belgeyi oluşturur.
    """
    user_id: str                                    # users._id (string)
    session_id: UUID = Field(default_factory=uuid4) # Her oturum için benzersiz UUID
    title: Optional[str] = None                     # İlk mesajdan otomatik üretilir


class ConversationInDB(ConversationCreate):
    """
    MongoDB conversations koleksiyonundaki tam belge.
    """
    message_count: int = 0
    is_archived: bool = False
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


class MessageCreate(BaseModel):
    """
    /chat/ endpoint'ine istemciden gelen istek gövdesi.
    session_id yoksa backend yeni bir Conversation oluşturur.
    file_base64 + file_mime_type dolu gelirse multimodal (görsel veya PDF) istek olarak işlenir.
    """
    user_id: str
    session_id: Optional[UUID] = None
    message: str
    file_base64: Optional[str] = None
    file_mime_type: Optional[str] = None


class ChatRequest(BaseModel):
    """
    Geriye dönük uyumluluk için korunan sade model.
    Sadece mesaj içerir; user/session bilgisi olmayan hızlı testler için.
    """
    message: str


class ChatResponse(BaseModel):
    """
    /chat/ endpoint'inin döndürdüğü yanıt.
    session_id frontend tarafından saklanarak sonraki isteklerde gönderilmeli.
    """
    reply: str
    session_id: UUID
