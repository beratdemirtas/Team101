"""
download_data.py
-----------------
Finansal Okuryazarlık Asistanı projesi için Kaggle üzerinden otomatik
indirilebilen veri setlerini çeker.

Kullanmadan önce:
    pip install -r requirements.txt
    Kaggle API key kurulumu: https://www.kaggle.com/docs/api
    (kaggle.json dosyasını ~/.kaggle/kaggle.json altına koy)

Çalıştırma:
    python download_data.py

NOT: PISA (OECD) ve SPK/RAG_Egitim_Verileri setleri manuel indirme
gerektirir (lisans onayı / web sayfası kaydı). Detaylar README.md içinde.
"""

import os
import subprocess
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# (kaggle dataset id, hedef klasör adı)
KAGGLE_DATASETS = [
    ("gokhankesler/borsa-istanbul-turkish-stock-exchange-dataset", "borsa_istanbul_kaggle"),
    ("uciml/istanbul-stock-exchange", "istanbul_stock_exchange_uci"),
    ("winvoker/turkishsentimentanalysisdataset", "turkish_sentiment_analysis_dataset"),
    ("mustfkeskin/turkish-movie-sentiment-analysis-dataset", "turkish_movie_sentiment_dataset"),
]

MANUAL_ONLY = [
    ("PISA Financial Literacy (OECD)", "pisa_dataset",
     "https://www.oecd.org/en/data/datasets/pisa-2022-database.html"),
    ("RAG Eğitim Verileri v1 (SPK/Borsa İstanbul)", "rag_egitim_verileri_v1",
     "spk.gov.tr üzerinden manuel kaydedilmiş web sayfaları"),
    ("SPK Yatırımcı Bilgilendirme Kitapçıkları", "spk_yatirimci_bilgilendirme_kitapciklari",
     "https://spk.gov.tr/yatirimcilar/yatirimci-bilgilendirme-kitapciklari"),
]


def check_kaggle_cli():
    try:
        subprocess.run(["kaggle", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_kaggle_dataset(dataset_id: str, folder_name: str):
    target = DATA_DIR / folder_name
    target.mkdir(parents=True, exist_ok=True)
    print(f"→ İndiriliyor: {dataset_id} → {target}")
    try:
        subprocess.run(
            ["kaggle", "datasets", "download", "-d", dataset_id, "-p", str(target), "--unzip"],
            check=True,
        )
        print(f"  ✔ Tamamlandı: {folder_name}")
    except subprocess.CalledProcessError as e:
        print(f"  ✘ Hata: {dataset_id} indirilemedi ({e})")


def main():
    if not check_kaggle_cli():
        print("HATA: 'kaggle' CLI bulunamadı. Kurulum için: pip install kaggle")
        print("Ardından API key'i şu adresten al: https://www.kaggle.com/docs/api")
        sys.exit(1)

    DATA_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print("Kaggle veri setleri indiriliyor...")
    print("=" * 60)
    for dataset_id, folder_name in KAGGLE_DATASETS:
        download_kaggle_dataset(dataset_id, folder_name)

    print("\n" + "=" * 60)
    print("Manuel indirme gereken veri setleri (otomatik çekilemez):")
    print("=" * 60)
    for name, folder_name, source in MANUAL_ONLY:
        (DATA_DIR / folder_name).mkdir(parents=True, exist_ok=True)
        print(f"  • {name}")
        print(f"    Klasör: data/{folder_name}/")
        print(f"    Kaynak: {source}\n")

    print("Detaylı talimatlar için README.md dosyasına bak.")


if __name__ == "__main__":
    main()
