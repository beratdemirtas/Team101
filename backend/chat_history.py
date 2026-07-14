from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorDatabase

CHAT_HISTORY_COLLECTION = "ChatHistory"
MAX_HISTORY_MESSAGES = 10  # son 5 karsilikli tur (kullanici + mentor)


async def get_chat_history(
    db: AsyncIOMotorDatabase, user_id: str, limit: int = MAX_HISTORY_MESSAGES
) -> list[dict]:
    """Kullanicinin son mesajlarini eskiden yeniye sirali dondurur."""
    collection = db[CHAT_HISTORY_COLLECTION]
    cursor = collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
    docs = await cursor.to_list(length=limit)
    docs.reverse()
    return [{"role": doc["role"], "content": doc["content"]} for doc in docs]


async def save_chat_message(
    db: AsyncIOMotorDatabase, user_id: str, role: str, content: str
) -> None:
    collection = db[CHAT_HISTORY_COLLECTION]
    await collection.insert_one(
        {
            "user_id": user_id,
            "role": role,
            "content": content,
            "created_at": datetime.now(timezone.utc),
        }
    )
