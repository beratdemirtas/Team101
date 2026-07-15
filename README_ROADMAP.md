# Fin101 — Proje Yol Haritası & Eksik Görevler

> **Son Güncelleme:** 2026-07-15
> **Aktif Dal:** `main`
> **Durum Özeti:** Backend MVP + RAG + Sohbet Hafızası + Temel Frontend tamamlandı. Proje Sprint 3 ile sonlanıyor.

---

## ✅ Tamamlanan Özellikler

### Backend
| Modül | Durum | Açıklama |
|---|---|---|
| FastAPI + Motor | ✅ | Async MongoDB bağlantısı, lifespan yönetimi |
| Pydantic Modelleri | ✅ | `UserCreate`, `UserInDB`, `UserResponse`, `ChatMessage`, `ConversationCreate`, `MessageCreate`, `ChatResponse` |
| `POST /users/` | ✅ | Kullanıcı kaydı, duplicate e-posta koruması |
| `POST /chat/` | ✅ | Hafızalı RAG endpoint'i (`session_id` yönetimi) |
| `GET /market/price/{ticker}` | ✅ | yfinance anlık fiyat |
| `GET /market/history/{ticker}` | ✅ | yfinance tarihsel OHLCV |
| `GET /news/market` | ✅ | Finnhub genel piyasa haberleri |
| `GET /news/company/{symbol}` | ✅ | Finnhub şirket haberleri |
| RAG Pipeline | ✅ | ChromaDB + `all-MiniLM-L6-v2` + Gemini 2.5 Flash |
| Sohbet Hafızası | ✅ | `conversations` + `messages` MongoDB koleksiyonları |
| Guardrails | ✅ | `check_user_input` + `check_assistant_output` (LLM tabanlı) |
| CORS | ✅ | `localhost:3000` ve `localhost:5173` izinli |

### Frontend
| Sayfa / Bileşen | Durum | Açıklama |
|---|---|---|
| Chatbot (`ChatView`) | ✅ | `session_id` yönetimi, Markdown render, Typewriter efekti |
| Dashboard | ✅ | `getMarketPrice` ile anlık hisse fiyat kartları |
| Haberler (`NewsMock`) | ✅ | `getMarketNews` ile Finnhub haberleri, kategori filtreleme |
| Profil (`ProfileMock`) | ✅ | Statik iskelet (XP bar, risk profili, ilgi alanları) |
| `api.js` servis katmanı | ✅ | `sendChatMessage`, `getMarketPrice`, `getMarketHistory`, `getMarketNews`, `getCompanyNews` |

---

## 🚀 Sprint 3 — Kalan Kritik Görevler

> Sprint 3, projenin **son ve tamamlayıcı** aşamasıdır. Aşağıdaki görevler projenin çekirdek işlevselliği için zorunludur.

---

### 1. Kimlik Doğrulama Sistemi (JWT Auth)

**Neden kritik:** Şu an tüm endpoint'ler açık; `user_id` sabit `"demo-user"` değeri kullanılıyor. Auth olmadan kullanıcıya özel hiçbir veri gösterilemez.

**Backend:**
- [ ] `python-jose` + `passlib[bcrypt]` kurulumu ve `requirements.txt`'e eklenmesi
- [ ] `models.py`'e `hashed_password` alanı eklenmesi
- [ ] `POST /auth/register` — şifreyi hash'leyip `users` koleksiyonuna kayıt
- [ ] `POST /auth/login` — kimlik doğrulama + JWT `access_token` üretimi
- [ ] FastAPI `Security(oauth2_scheme)` ile `/chat/`, `/users/me` endpoint'lerine token koruması

**Frontend:**
- [ ] Login ve Register form sayfaları
- [ ] JWT token'ı `localStorage`'da saklama
- [ ] `api.js`'teki tüm isteklere `Authorization: Bearer <token>` header'ı eklenmesi
- [ ] `sendChatMessage` içindeki `"demo-user"` sabitinin token'dan alınan gerçek `user_id` ile değiştirilmesi
- [ ] Oturum açılmamışsa login sayfasına yönlendirme

**İlgili dosyalar:** `backend/models.py`, `backend/main.py`, `frontend/src/services/api.js`, `frontend/src/pages/`

---

### 2. Profil Sayfasının MongoDB ile Eşleştirilmesi

**Neden kritik:** `ProfileMock.jsx` tamamen statik veri gösteriyor; Auth tamamlanınca gerçek kullanıcı verisi bağlanmalı.

**Backend:**
- [ ] `GET /users/me` endpoint'i (token'dan `user_id` çekerek ilgili belgeyi döndürür)
- [ ] `PUT /users/me` endpoint'i (isim, risk_profile, ilgi alanları güncellemesi)

**Frontend:**
- [ ] `ProfileMock.jsx`'e `useEffect` + `GET /users/me` çağrısı
- [ ] `xp_score`, `level`, `badges`, `risk_profile`, `virtual_balance` alanlarının dinamik gösterimi
- [ ] Profil düzenleme formu (isim, risk profili, ilgi alanları)

**İlgili dosyalar:** `backend/main.py`, `frontend/src/pages/ProfileMock.jsx`

---

### 3. Borsa Simülasyonu Sayfasının Aktifleştirilmesi

**Neden kritik:** `SimulationMock.jsx` tamamen boş iskelet; projenin ana öğrenme aracıdır.

**Veri Kaynağı Seçenekleri:**
- Yfinance `getMarketHistory` (dinamik, anlık) — **önerilen**
- Kaggle BIST-100 CSV dataset (statik ama offline çalışır)

**Backend:**
- [ ] `POST /transactions/` endpoint'i (al/sat işlemi kaydı → `transactions` koleksiyonu)
- [ ] `GET /portfolio/me` endpoint'i (kullanıcının portföy özeti → `portfolios` koleksiyonu)
- [ ] `models.py`'deki `Transaction` ve `Portfolio` Pydantic şemalarının aktivasyonu

**Frontend:**
- [ ] `recharts` veya `chart.js` ile OHLCV mum/çizgi grafik bileşeni
- [ ] Hisse arama + seçim arayüzü
- [ ] Sanal al/sat formu (miktar, fiyat, onay)
- [ ] Portföy özeti tablosu (holding, ortalama maliyet, kâr/zarar)
- [ ] Dashboard'a portföy özet kartı entegrasyonu

**İlgili dosyalar:** `backend/main.py`, `backend/models.py`, `frontend/src/pages/SimulationMock.jsx`, `frontend/src/pages/DashboardMock.jsx`

---

## 🗂️ Gelecek Vizyonu (Backlog)

> Aşağıdaki özellikler projenin **çekirdeği için zorunlu değildir** ve herhangi bir sprint'e bağlı değildir. Proje ilerledikçe değerlendirilebilir.

| Özellik | Açıklama |
|---|---|
| **XP / Gamification** | Her `/chat/` yanıtından sonra `xp_score` artışı, seviye sistemi, liderlik tablosu |
| **Yatırımcı Meydanı** | Sosyal ağ gönderileri, like/yorum, moderasyon (`investor_square` koleksiyonu) |
| **Rate Limiting** | `slowapi` ile IP başına `/chat/` istek sınırı |
| **Global Hata Yönetimi** | `@app.exception_handler` ile standart hata formatı |
| **Test Coverage** | `pytest` + `httpx` + `pytest-asyncio` |
| **Docker** | `Dockerfile` + `docker-compose.yml` |
| **Deployment** | Railway / Render (backend) + Vercel / Netlify (frontend) |
| **Türkçe Embedding** | `intfloat/multilingual-e5-base` — Türkçe metinlerde daha yüksek kalite |
| **RAG Kaynak Alıntısı** | Asistan yanıtına kaynak PDF chunk bilgisi eklenmesi |
| **Atlas Vector Search** | ChromaDB → MongoDB Atlas Vector Search geçişi (production) |

---

## Ortam Değişkenleri Referansı

### `backend/.env`
```env
MONGO_URI=mongodb+srv://...
DATABASE_NAME=Fin101DB
GEMINI_API_KEY=...
FINNHUB_API_KEY=...
```

### `frontend/.env.local`
```env
VITE_API_URL=http://localhost:8000
```

---

## Geliştirme Ortamını Başlatma

```powershell
# Terminal 1 — Backend (backend/ klasöründe, venv aktifken)
uvicorn main:app --reload

# Terminal 2 — Frontend (frontend/ klasöründe)
npm run dev
```

**Swagger UI:** http://localhost:8000/docs
**Frontend:** http://localhost:5173

---

## Koleksiyon Durumu

| Koleksiyon | Durum | Bağımlılık |
|---|---|---|
| `users` | ✅ Aktif | Kayıt + profil |
| `conversations` | ✅ Aktif | Sohbet oturumları |
| `messages` | ✅ Aktif | Tekil mesajlar |
| `transactions` | 🔴 Sprint 3 | Borsa işlemleri |
| `portfolios` | 🔴 Sprint 3 | Portföy özeti |
| `news_cache` | 🗂️ Backlog | Haber TTL cache |
| `investor_square` | 🗂️ Backlog | Sosyal ağ |
