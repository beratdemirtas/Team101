# 📊 Data Klasörü — Kaynaklar ve İndirme Talimatları

Bu klasörde **ham veri dosyaları tutulmaz** (repo boyutunu şişirmemek için `.gitignore` ile hariç tutulmuştur). Bunun yerine her veri setinin nereden ve nasıl indirileceği aşağıda listelenmiştir.

Otomatik indirilebilenler için `download_data.py` scriptini çalıştırman yeterli:

```bash
pip install -r requirements.txt
python download_data.py
```

Kaggle API key'i olmayanlar önce şu adımı yapmalı: https://www.kaggle.com/docs/api → `kaggle.json` dosyasını `~/.kaggle/` altına koy.

---

## 1. Borsa İstanbul (Kaggle)
- **Klasör:** `data/borsa_istanbul_kaggle/`
- **Kaynak:** https://www.kaggle.com/datasets/gokhankesler/borsa-istanbul-turkish-stock-exchange-dataset
- **Format:** CSV
- **İndirme:** `download_data.py` içindeki `KAGGLE_DATASETS` listesinde otomatik, ya da manuel:
  ```bash
  kaggle datasets download -d gokhankesler/borsa-istanbul-turkish-stock-exchange-dataset -p data/borsa_istanbul_kaggle --unzip
  ```

## 2. Istanbul Stock Exchange (Kaggle — UCI)
- **Klasör:** `data/istanbul_stock_exchange_uci/`
- **Kaynak:** https://www.kaggle.com/datasets/uciml/istanbul-stock-exchange
- **Format:** CSV
- **İndirme:**
  ```bash
  kaggle datasets download -d uciml/istanbul-stock-exchange -p data/istanbul_stock_exchange_uci --unzip
  ```

## 3. PISA Financial Literacy Dataset (OECD)
- **Klasör:** `data/pisa_dataset/`
- **Kaynak:** https://www.oecd.org/en/data/datasets/pisa-2022-database.html
- **Format:** SPSS (.sav) / SAS — PUF (Public Use File)
- **İndirme:** Manuel — OECD'nin PUF erişim formunu doldurup onay aldıktan sonra "Financial Literacy data file (SPSS)" linkine tıkla, indirilen `.sav` dosyasını bu klasöre koy. (API/otomatik indirme desteklemiyor.)

## 4. RAG Eğitim Verileri v1 (SPK / Borsa İstanbul kaynaklı)
- **Klasör:** `data/rag_egitim_verileri_v1/`
- **Kaynak:** spk.gov.tr ve ilgili yatırımcı eğitim siteleri
- **Format:** HTML (kaydedilmiş web sayfaları)
- **İndirme:** Manuel — tarayıcıdan "Farklı Kaydet → Web Sayfası, Tamamı" ile kaydedildi.
- ⚠️ **Dış paylaşıma kapalı** — SPK içerikleri yeniden yayınlama izni gerektirir, yalnızca RAG embedding için iç kullanımda tutulmalı.

## 5. SPK Yatırımcı Bilgilendirme Kitapçıkları
- **Klasör:** `data/spk_yatirimci_bilgilendirme_kitapciklari/`
- **Kaynak:** https://spk.gov.tr/yatirimcilar/yatirimci-bilgilendirme-kitapciklari
- **Format:** PDF
- **İndirme:** Manuel — sayfadaki kitapçık linklerinden tek tek indirilir.
- ⚠️ **Dış paylaşıma kapalı** — aynı kısıtlama yukarıdaki gibi geçerlidir.

## 6. Turkish Sentiment Analysis Dataset (Winvoker)
- **Klasör:** `data/turkish_sentiment_analysis_dataset/`
- **Kaynak:** https://www.kaggle.com/datasets/winvoker/turkishsentimentanalysisdataset
- **Format:** CSV
- **İndirme:**
  ```bash
  kaggle datasets download -d winvoker/turkishsentimentanalysisdataset -p data/turkish_sentiment_analysis_dataset --unzip
  ```

## 7. Turkish Movie Sentiment Dataset
- **Klasör:** `data/turkish_movie_sentiment_dataset/`
- **Kaynak:** https://www.kaggle.com/datasets/mustfkeskin/turkish-movie-sentiment-analysis-dataset
- **Format:** CSV
- **İndirme:**
  ```bash
  kaggle datasets download -d mustfkeskin/turkish-movie-sentiment-analysis-dataset -p data/turkish_movie_sentiment_dataset --unzip
  ```

---

## Canlı veri (statik dosya yerine)
BIST/global hisse verisi için statik CSV yerine `yfinance` ile anlık çekmek daha güncel sonuç verir:

```python
import yfinance as yf
data = yf.download("XU100.IS", start="2015-01-01", end="2026-07-13")
```

---

## Not
- Kaggle setleri `download_data.py` ile otomatik çekilebilir.
- PISA ve SPK/RAG setleri **manuel indirme** gerektirir (API/lisans kısıtlaması).
- Hiçbir ham veri dosyası (`.csv`, `.sav`, `.pdf`, `.html`, `.zip`) git'e eklenmemelidir — bkz. `.gitignore`.
