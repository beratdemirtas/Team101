# Fin101 — Proje Yol Haritası & Eksik Görevler

> **Son Güncelleme:** 2026-07-15
> **Dal:** feature/database → main'e merge hazır
> **Durum Özeti:** Backend MVP + RAG + Sohbet Hafızası + Temel Frontend tamamlandı.

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
| Guardrails | ✅ | `check_user_input` + `check_assistant_output` (Gemini LLM tabanlı) |
| CORS | ✅ | `localhost:3000` ve `localhost:5173` izinli |

### Frontend
| Sayfa / Bileşen | Durum | Açıklama |
|---|---|---|
| Chatbot (`ChatView`) | ✅ | `session_id` yönetimi, Markdown render, Typewriter efekti |
| Dashboard | ✅ | `getMarketPrice` ile 4 hisse anlık fiyat kartları |
| Haberler (`NewsMock`) | ✅ | `getMarketNews` ile Finnhub haberleri, kategori filtreleme |
| Profil (`ProfileMock`) | ✅ | Statik iskelet (XP bar, risk profili, ilgi alanları) |
| `api.js` servis katmanı | ✅ | `sendChatMessage`, `getMarketPrice`, `getMarketHistory`, `getMarketNews`, `getCompanyNews` |

---

## 🔴 Eksik — Yüksek Öncelik (Sprint 3)

### 1. Kimlik Doğrulama Sistemi (JWT Auth)

**Neden gerekli:** Şu an `/chat/` endpoint'ine herkes erişebilir. `user_id` sabit `"demo-user"` string'i.

**Yapılacaklar:**
- [ ] `python-jose` + `passlib` kurulumu
- [ ] `POST /auth/register` — şifre bcrypt hash'i ile `users` koleksiyonuna kayıt
- [ ] `POST /auth/login` — JWT token üretimi (`access_token`, `refresh_token`)
- [ ] FastAPI `Security` dependency ile tüm endpoint'lere `Bearer` token koruması
- [ ] `models.py`'e `hashed_password` alanı eklenmesi (şu an yorum satırı)
- [ ] Frontend: login/register form sayfası
- [ ] Frontend: JWT token'ı `localStorage`'da saklama ve her istekte `Authorization` header'ı gönderme
- [ ] `demo-user` sabit değerini gerçek `user_id` ile değiştirme

**İlgili Dosyalar:** `backend/models.py`, `backend/main.py`, `frontend/src/services/api.js`, `frontend/src/pages/`

---

### 2. Profil Sayfasının MongoDB ile Eşleştirilmesi

**Neden gerekli:** `ProfileMock.jsx` şu an tamamen statik veri gösteriyor.

**Yapılacaklar:**
- [ ] Auth tamamlandıktan sonra `GET /users/me` endpoint'i eklenmesi
- [ ] `ProfileMock.jsx`'e `useEffect` + `GET /users/me` çağrısı
- [ ] `xp_score`, `level`, `badges`, `risk_profile`, `virtual_balance` alanlarının dinamik gösterimi
- [ ] Profil düzenleme: `PUT /users/me` endpoint'i + form bileşeni
- [ ] Avatar yükleme (opsiyonel, S3 veya base64)

**İlgili Dosyalar:** `backend/main.py`, `frontend/src/pages/ProfileMock.jsx`

---

## 🟠 Eksik — Orta Öncelik (Sprint 4)

### 3. Borsa Simülasyonu Sayfasının Aktifleştirilmesi

**Neden gerekli:** `SimulationMock.jsx` tamamen boş iskelet.

**Yapılacaklar:**
- [ ] Kaggle veri seti entegrasyonu (örn: BIST-100 tarihsel fiyat CSV)
  - Öneri: `akfin` veya `Kaggle BIST dataset`
  - Alternatif: yfinance `getMarketHistory` ile dinamik çekme
- [ ] `recharts` veya `chart.js` ile OHLCV grafik bileşeni
- [ ] Sanal al/sat arayüzü: hisse seçimi, miktar girişi, işlem butonu
- [ ] `POST /transactions/` backend endpoint'i (`transactions` koleksiyonu — models.py'de şema hazır)
- [ ] `GET /portfolio/me` endpoint'i (portföy özeti)
- [ ] Dashboard'a portföy özet kartı entegrasyonu

**İlgili Dosyalar:** `backend/main.py`, `backend/models.py`, `frontend/src/pages/SimulationMock.jsx`, `frontend/src/pages/DashboardMock.jsx`

---

### 4. Kullanıcı XP / Gamification Sistemi

**Neden gerekli:** `UserInDB` modelinde `xp_score`, `level`, `badges` alanları var ama hiç güncellenmeyebilir.

**Yapılacaklar:**
- [ ] Her başarılı `/chat/` yanıtından sonra `xp_score += 10` güncellenmesi
- [ ] XP eşiğine göre `level` otomatik artışı
- [ ] Liderlik tablosu endpoint'i: `GET /leaderboard/` (`users` üzerinde `xp_score` desc sıralama)
- [ ] Dashboard'a liderlik tablosu widget'ı

---

## 🟡 Eksik — Düşük Öncelik / İleriki Sprint (Sprint 5+)

### 5. Yatırımcı Meydanı (Sosyal Ağ)

- [ ] `investor_square` MongoDB koleksiyonu aktivasyonu (şema `db_analysis.md`'de hazır)
- [ ] `POST /posts/` — gönderi oluşturma
- [ ] `GET /posts/feed` — akış
- [ ] Like / Yorum sistemi
- [ ] Moderasyon: `is_flagged` alanı + admin paneli

### 6. Altyapı & Güvenlik

- [ ] `slowapi` ile rate limiting (`/chat/` için IP başına dakika limiti)
- [ ] Global FastAPI exception handler (`@app.exception_handler`)
- [ ] `pytest` + `httpx` ile temel API testleri
- [ ] Docker: `Dockerfile` + `docker-compose.yml`
- [ ] Deployment: Railway / Render (backend) + Vercel / Netlify (frontend)
- [ ] MongoDB Atlas index'leri: `email` (unique), `session_id`, `conversation_id + created_at`

### 7. RAG İyileştirmeleri

- [ ] `intfloat/multilingual-e5-base` embedding modeline geçiş (Türkçe metinlerde daha yüksek kalite)
- [ ] ChromaDB yerine Atlas Vector Search entegrasyonu (production'da)
- [ ] Kaynak alıntısı: asistan yanıtına hangi PDF chunk'ından alındığını ekleme (`rag_sources` alanı)

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

## Koleksiyon & Şema Referansı

Detaylı MongoDB şema tasarımı ve koleksiyon açıklamaları için:
→ Bkz. [Antigravity Analiz Raporu](/.agents/) veya `db_analysis.md` (proje asistan çıktısı)

| Koleksiyon | Durum | Açıklama |
|---|---|---|
| `users` | ✅ Aktif | Kayıt + profil |
| `conversations` | ✅ Aktif | Sohbet oturumları |
| `messages` | ✅ Aktif | Tekil mesajlar |
| `transactions` | 🔴 Eksik | Borsa işlemleri |
| `portfolios` | 🔴 Eksik | Portföy özeti |
| `news_cache` | 🟡 Opsiyonel | Haber TTL cache |
| `investor_square` | 🟡 Sprint 5+ | Sosyal ağ |
