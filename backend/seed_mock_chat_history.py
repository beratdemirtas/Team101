"""Sohbet hafizasi ozelligini test etmek icin ornek (mock) veri ekler.

Kullanim:
    python seed_mock_chat_history.py

Calistirdiktan sonra /chat/ endpoint'ini su gövdeyle deneyebilirsiniz:
    {"user_id": "mock_user_001", "message": "Peki bunu benim durumuma nasil uygularim?"}
Mentor, asagidaki mock gecmisi bagalam olarak gorup "bunu" kelimesinin neye
(bilesik faize) atif yaptigini anlayabilmelidir.
"""

import asyncio
from datetime import datetime, timedelta, timezone

from database import connect_db, close_db, get_database

MOCK_USER_ID = "mock_user_001"

MOCK_MESSAGES = [
    {"role": "user", "content": "Merhaba, bilesik faiz nedir?"},
    {
        "role": "assistant",
        "content": (
            "Guzel bir baslangic noktasi! Sence paranı bir yil bekletip sadece "
            "anaparan uzerinden faiz almakla, her yil kazandigin faizi de "
            "anaparana ekleyip bir sonraki yil onun uzerinden de faiz almak "
            "arasinda ne fark olur?"
        ),
    },
    {"role": "user", "content": "Sanirim ikincisinde zamanla daha cok kazanirim?"},
    {
        "role": "assistant",
        "content": (
            "Neden oyle dusundugunu biraz daha acar misin? Faizin faizi "
            "kazanmasi, uzun vadede sana nasil bir avantaj saglar?"
        ),
    },
]


async def seed() -> None:
    await connect_db()
    db = get_database()
    collection = db["ChatHistory"]

    existing = await collection.count_documents({"user_id": MOCK_USER_ID})
    if existing:
        print(f"Mock veriler zaten mevcut ({existing} mesaj, user_id='{MOCK_USER_ID}'). Atlaniyor.")
        await close_db()
        return

    now = datetime.now(timezone.utc)
    docs = [
        {
            "user_id": MOCK_USER_ID,
            "role": item["role"],
            "content": item["content"],
            "created_at": now + timedelta(seconds=i),
        }
        for i, item in enumerate(MOCK_MESSAGES)
    ]
    await collection.insert_many(docs)
    print(f"{len(docs)} mock mesaj eklendi. user_id='{MOCK_USER_ID}'")
    await close_db()


if __name__ == "__main__":
    asyncio.run(seed())
