# Fin101 — Teknik Dokümantasyon ve Yol Haritası

> **Belge Tarihi:** 5 Temmuz 2026 (v0.2.0 — güncellendi)
> **Versiyon:** 0.2.0 (Backend MVP Tamamlandı)
> **Durum:** ✅ Backend MVP Tamamlandı — Frontend Entegrasyonuna Hazır

---

## 1. Mevcut Mimari Analizi

### 1.1 Teknoloji Yığını (Tech Stack)

| Katman | Teknoloji | Rol |
|---|---|---|
| **API Framework** | FastAPI 0.x | Asenkron REST API sunucusu |
| **ASGI Sunucusu** | Uvicorn | Geliştirme + prod server |
| **Veritabanı** | MongoDB Atlas | Kullanıcı verisi ve sohbet geçmişi |
| **DB Driver** | Motor (async) | FastAPI uyumlu MongoDB bağlantısı |
| **Veri Doğrulama** | Pydantic v2 | Şema validasyonu ve tip güvenliği |
| **LLM** | Gemini 2.5 Flash | Yanıt üretimi (cached) |
| **RAG Orkestrasyonu** | LangChain v0.3+ | Retrieval zinciri yönetimi |
| **Embedding Modeli** | `all-MiniLM-L6-v2` | Metin vektörleştirme (local) |
| **Vektör Veritabanı** | ChromaDB | Semantik arama / chunk depolama |
| **PDF Okuyucu** | PyMuPDF | Yüksek uyumlu PDF metin çıkarımı |
| **Ortam Yönetimi** | python-dotenv | `.env` değişken yükleyici |

### 1.2 Dosya Yapısı

```
Fin101_Project/
├── .gitignore                  ← Python, venv, .env, IDE kalıntıları
└── backend/
    ├── .gitignore              ← chroma_store/, .env (backend özgü)
    ├── .env                    ← Gizli anahtarlar (git'e GİTMEZ)
    ├── requirements.txt        ← Tüm bağımlılıklar
    ├── config.py               ← Ortam değişkeni merkezi yönetim
    ├── database.py             ← Motor async bağlantı yaşam döngüsü
    ├── models.py               ← Pydantic şemaları
    ├── rag.py                  ← RAG motoru (kalp) — LLM cached
    ├── main.py                 ← FastAPI app + CORS + DI + endpoint'ler
    ├── chroma_store/           ← ChromaDB persist klasörü (git'e GİTMEZ)
    └── rag_data/
        └── Yatirim_Yaparken_5_Baski_opt.pdf
```

### 1.3 Sistem Mimarisi — Veri Akışı

```mermaid
flowchart TD
    A[Frontend / Postman] -->|POST /chat/| B[FastAPI - main.py]
    B --> C[ask_mentor - rag.py]
    C --> D{ChromaDB\nchroma_store/ mevcut mu?}
    D -->|Evet| E[Mevcut vektör deposu yükle]
    D -->|Hayır| F[PyMuPDF ile PDF oku]
    F --> G[RecursiveCharacterTextSplitter\n1000 char / 150 overlap]
    G --> H[HuggingFace Embeddings\nall-MiniLM-L6-v2]
    H --> I[ChromaDB'ye persist et]
    E --> J[Retriever: k=4 semantik arama]
    I --> J
    J --> K[Bağlam oluştur]
    K --> L[Gemini 2.5 Flash\nCached LLM nesnesi]
    L --> M[reply: ... JSON yanıtı]
    M --> A
```

### 1.4 Mevcut API Endpoint'leri

| Method | Path | Açıklama |
|---|---|---|
| `GET` | `/` | Sağlık kontrolü |
| `POST` | `/users/` | Yeni kullanıcı oluşturma (DI ile DB) |
| `POST` | `/chat/` | RAG zinciriyle Sokratik Mentor yanıtı |

**Swagger UI:** `http://127.0.0.1:8000/docs`

---

## 2. Tamamlanan Başarılar

### ✅ FastAPI + MongoDB Atlas Entegrasyonu
Motor kütüphanesi `lifespan` ile yönetiliyor; bağlantı uygulama açılışında kurulup kapanışında düzgün sonlandırılıyor. Kullanıcı oluşturma endpoint'i duplicate e-posta koruması içeriyor.

### ✅ Modüler Mimari
Her sorumluluğun kendi dosyasında yaşaması (`config`, `database`, `models`, `rag`, `main`) ilerideki büyümeyi doğrudan mümkün kılıyor.

### ✅ LangChain v0.3+ Modüler Import Geçişi
`langchain.text_splitter` → `langchain_text_splitters`, `langchain.schema` → `langchain_core.messages` geçişleri tamamlandı.

### ✅ PDF Okuma Sağlamlığı
`PyPDFLoader` → `PyMuPDFLoader` geçişiyle sıkıştırılmış PDF'lerin okunması mümkün. Her PDF için `try/except` ile izole hata yönetimi eklendi.

### ✅ RAG Dosya Yolu Kararlılığı
`Path(__file__).resolve().parent` ile mutlak yol hesaplaması; çalışma dizininden bağımsız.

### ✅ ChromaDB Lazy-Load + Cache
Vektör deposu yalnızca ilk istekte oluşturuluyor, ardından bellekte tutuluyor (`_vector_store` global).

### ✅ Güvenlik — `.gitignore` Yapılandırması *(v0.2.0)*
`backend/.gitignore` oluşturuldu. `chroma_store/` ve `.env` artık kesinlikle Git'e gitmiyor. Gizli anahtarlar ve türetilmiş dosyalar repository dışında tutuluyor.

### ✅ CORS Middleware Entegrasyonu *(v0.2.0)*
`CORSMiddleware` `main.py`'e eklendi. React (`:3000`) ve Vite (`:5173`) geliştirme sunucuları için cross-origin isteklerine izin verildi. Frontend entegrasyonu artık teknik engel olmadan başlayabilir.

### ✅ LLM Cache Mekanizması *(v0.2.0)*
`_build_llm()` → `_get_llm()` dönüşümüyle `ChatGoogleGenerativeAI` nesnesi modül ömrü boyunca **tek bir kez** oluşturuluyor. Her `/chat/` isteğindeki gereksiz nesne yaratma maliyeti ortadan kalktı.

### ✅ FastAPI Dependency Injection — DB Bağlantısı *(v0.2.0)*
Global `client` değişkenine doğrudan erişim yerine `Depends(get_db)` pattern'ı uygulandı. `DatabaseDep` tip takma adıyla endpoint imzaları temiz ve test edilebilir hale geldi.

---

## 3. Üretim Hazırlığı Analizi

### 🏭 Ne Kadar "Production-Ready"iz?

```
[██████████░░░░░░░░░░] ~50%
```

| Alan | Durum | Açıklama |
|---|---|---|
| API Altyapısı | ✅ Hazır | FastAPI, async, CORS |
| Veri Doğrulama | ✅ Hazır | Pydantic v2 şemaları |
| RAG Pipeline | ✅ Hazır | ChromaDB + Gemini entegre |
| Güvenlik (.env, .gitignore) | ✅ Hazır | Sırlar git'ten korunuyor |
| **Kimlik Doğrulama (Auth)** | ❌ Eksik | Herkes her endpoint'e erişebilir |
| **Sohbet Hafızası** | ❌ Eksik | Her istek stateless, geçmiş yok |
| **Hata Yönetimi (Global)** | 🟡 Kısmi | Sadece RAG'da loglama var |
| **Test Coverage** | ❌ Eksik | Hiç test yazılmadı |
| **Rate Limiting** | ❌ Eksik | DDoS/abuse koruması yok |
| **Docker / Containerization** | ❌ Eksik | Deployment hazırlığı yok |

> **Değerlendirme:** Backend, **güvenli bir geliştirme ve demo ortamı** için hazır. Canlıya almak için Auth ve Rate Limiting zorunlu; diğerleri ikinci sprint'te ele alınabilir.

---

## 4. Aktif Sprint — Öncelikli Görevler

### 🚀 Sprint 2 Hedefleri

#### 4.1 Sohbet Geçmişi Yönetimi (Session Management)

**Hedef:** Her kullanıcıya ait konuşma geçmişini MongoDB'ye kaydetmek ve `ask_mentor`'a bağlam olarak vermek.

**Yapılacaklar Listesi:**

- [ ] `models.py`'e `ChatMessage` ve `Conversation` Pydantic şemaları ekle
  ```python
  class ChatMessage(BaseModel):
      role: Literal["user", "assistant"]
      content: str
      timestamp: datetime = Field(default_factory=datetime.utcnow)

  class Conversation(BaseModel):
      user_id: str
      messages: list[ChatMessage] = []
  ```
- [ ] MongoDB'de `Conversations` koleksiyonu oluştur
- [ ] `POST /chat/` endpoint'ini `user_id` alacak şekilde güncelle
- [ ] Her sorguda geçmiş mesajları DB'den çek, LangChain `ConversationBufferMemory`'e ver
- [ ] Her yeni mesaj çiftini (user + assistant) DB'ye kaydet

**Veri Akışı:**
```
/chat/ isteği (user_id + message)
  → MongoDB'den geçmiş çek
  → RAG retriever çalıştır
  → [Geçmiş + Bağlam + Soru] → Gemini
  → Yanıtı MongoDB'ye kaydet
  → Frontend'e dön
```

#### 4.2 React/Vite Frontend Entegrasyonu

**Hedef:** Backend API'yi tüketen, Sokratik Mentor arayüzünü sunan frontend.

**Yapılacaklar Listesi:**

- [ ] Frontend dizinini oluştur (`Fin101_Project/frontend/`)
- [ ] Vite + React projesi başlat: `npm create vite@latest . -- --template react`
- [ ] `.env.local` oluştur: `VITE_API_URL=http://localhost:8000`
- [ ] API istemci katmanı yaz (`src/api/mentor.js`):
  ```javascript
  export const askMentor = async (message) => {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/chat/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    return res.json(); // { reply: "..." }
  };
  ```
- [ ] Chat arayüzü komponenti: mesaj baloncukları, yükleme animasyonu
- [ ] Kullanıcı kayıt formu → `POST /users/` entegrasyonu
- [ ] Sohbet geçmişini state'te tut, scroll davranışı

---

## 5. Backlog — İleriki Sprintler

### 🟡 Önemli (Sprint 3)

| # | Görev | Açıklama |
|---|---|---|
| **5.1** | JWT Kimlik Doğrulama | `python-jose` + `fastapi-users`; tüm endpoint'leri koru |
| **5.2** | `risk_profile` tip kısıtlaması | `Literal["Düşük", "Orta", "Yüksek"]` — geçersiz değer girişini engelle |
| **5.3** | `UserResponse` şeması | `_id` ObjectId'yi `str` olarak döndür |
| **5.4** | Global hata yönetimi | `@app.exception_handler` ile standart hata formatı |

### 🟢 İyileştirme (Sprint 4+)

| # | Alan | Öneri |
|---|---|---|
| **5.5** | Türkçe Embedding | `intfloat/multilingual-e5-base` → Türkçe metinlerde daha yüksek kalite |
| **5.6** | Rate Limiting | `slowapi` ile IP başına istek sınırı |
| **5.7** | Test | `pytest` + `httpx` + `pytest-asyncio` |
| **5.8** | Docker | `Dockerfile` + `docker-compose.yml` (backend + MongoDB) |
| **5.9** | Deployment | Railway veya Render → backend; Atlas M0 → MongoDB |

---

## 6. Frontend ↔ Backend Bağlantı Rehberi

### CORS Durumu
```python
# main.py — Şu an aktif
allow_origins=["http://localhost:3000", "http://localhost:5173"]
# Canlıya alırken → ["https://fin101.yourdomain.com"]
```

### Environment Değişkenleri

| Ortam | Backend | Frontend |
|---|---|---|
| Geliştirme | `backend/.env` | `frontend/.env.local` |
| Production | Hosting env vars | Build-time injection |

---

## 7. Hızlı Başvuru Kartı

### Sunucuyu Başlatma
```powershell
# backend/ dizininde, venv aktifken:
uvicorn main:app --reload
```

### Yeni Paket Eklendiğinde
```powershell
pip install -r requirements.txt
```

### ChromaDB'yi Sıfırlama (PDF değiştiğinde)
```powershell
Remove-Item -Recurse -Force .\chroma_store
```

### Swagger UI
```
http://127.0.0.1:8000/docs
```

---

> **v0.1.0 → v0.2.0 Değişiklikleri:** `.gitignore` güvenliği, CORS middleware, LLM cache, Dependency Injection pattern uygulandı.
> Bir sonraki güncelleme: Sohbet geçmişi ve frontend entegrasyonu tamamlandığında.
