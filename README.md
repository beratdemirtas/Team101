# Team101 — Fin101

## Takım Üyeleri
* **Fatımanur Kantar** – Product Owner
* **Özlem Kılıç** – Scrum Master
* **Berat Muhammet Demirtaş** – Developer
* **Melike Kahraman** – Developer
* **İbrahim Emin İpek** – Developer

## Ürün Açıklaması
Bu proje, özellikle genç kullanıcılara yönelik geliştirilen yapay zekâ destekli bir finansal okuryazarlık ve yatırım bilgilendirme platformudur.
Platform, kullanıcıların finansal farkındalıklarını artırmayı ve borsa hakkında bilinçli kararlar alabilmelerini desteklemeyi amaçlamaktadır.

Kullanıcılar sanal bakiye ile borsa simülasyonu yaparak gerçek para riski olmadan alım-satım deneyimi kazanabilir. Ayrıca yapay zekâ destekli chatbot ve güncel finansal haberler sayesinde piyasa gelişmeleri takip edilebilir ve finansal konularda bilgi edinilebilir.

Ürün, yatırım tavsiyesi sunmak yerine bilgilendirici ve yönlendirici bir yaklaşım benimseyerek finansal okuryazarlığın gelişmesine katkı sağlamayı hedeflemektedir.

## Ürün Özellikleri

**💰 Sanal Borsa Simülasyonu**
* Sanal bakiye ile alım-satım işlemleri yapılabilir
* Gerçek para riski olmadan yatırım deneyimi kazanılır

**🤖 Yapay Zekâ Destekli Chatbot**
* Finansal konularda kullanıcı sorularını yanıtlar
* Bilgilendirici ve yönlendirici destek sağlar (RAG destekli Sokratik Mentor)

**📰 Piyasa ve Haber Takibi**
* Güncel borsa haberleri görüntülenir
* API aracılığıyla finansal gelişmeler takip edilir

**📊 Dashboard**
* Kullanıcı bakiye ve işlem geçmişi görüntülenir
* Tüm modüllere tek ekrandan erişim sağlanır

**👤 Kullanıcı Profili**
* Kullanıcı bilgileri ve hesap ayarları yönetilir

## Planlanan Sayfalar
* Dashboard
* Borsa Simülasyonu
* Haberler
* Chatbot
* Profil

## Hedef Kitle
* 18–35 yaş arası gençler ve genç profesyoneller
* Finansal okuryazarlığını geliştirmek isteyen bireyler
* Borsaya ve yatırım dünyasına yeni adım atan kullanıcılar
* Gerçek para riski olmadan yatırım deneyimi kazanmak isteyen kişiler
* Güncel piyasa gelişmelerini takip ederek bilinçli finansal kararlar almak isteyen kullanıcılar

---

## Kullanılacak Teknolojiler ve Mimari
Projemiz, temiz kod prensipleri ve modern yapay zeka orkestrasyonu gözetilerek geliştirilmektedir.

* **Proje Yönetimi ve Tasarım:** GitHub, Trello, Figma
* **Backend Framework:** FastAPI, Uvicorn (Asenkron mimari, Dependency Injection)
* **Yapay Zekâ ve LLM:** Google Gemini 2.5 Flash, HuggingFace (`all-MiniLM-L6-v2`)
* **RAG Orkestrasyonu:** LangChain v0.3, ChromaDB (Vektör Veritabanı)
* **Kalıcı Veritabanı:** MongoDB Atlas (Motor async driver)
* **Veri İşleme:** PyMuPDF, Pydantic v2
* **Finansal Veri API'leri:** (İlerleyen sprintlerde entegre edilecek)

---

## Proje Yönetimi ve Sprint Kanıtları

* **Product Backlog URL:** [Team101 Trello Board](https://trello.com/invite/b/6a3d8286def1d4972225c9b8/ATTI1dc614b3193520b51446148521c146a8DF7982DE/sprintplan)

### Sprint 1 Çıktıları
* **Backlog Düzeni ve Story Seçimleri:** İlk sprint için ekip kapasitesine uygun puanlamalar yapılmış, Story'ler mantıksal Task'lere bölünmüştür.
* **Daily Scrum Notları:** Takım içi iletişim günlük olarak yürütülmektedir. (Toplantı notları repodaki ilgili klasöre eklenecektir)[cite: 2].
* **Sprint Board Durumu:** <img width="1920" height="838" alt="Ekran görüntüsü 2026-07-05 134912" src="https://github.com/user-attachments/assets/0398d9f7-c464-4a32-a392-8c6cd0968be9" />

* **Ürün Durumu:**  Sprint 1 itibarıyla yapay zeka tarafında RAG (Retrieval-Augmented Generation) mimarisinin temelleri atılmış; LangChain ve Gemini entegrasyonu ile finansal dokümanları okuyup Sokratik cevaplar üreten API endpoint'leri çalışır hale getirilmiştir. Veritabanı tarafında MongoDB bağlantısı altyapısı kurulmuş olup, veri tablolarının (koleksiyonların) oluşturulması ve sohbet hafızasının eklenmesi sonraki sprintlere planlanmıştır[cite: 2].
* **Detaylı Teknik Dokümantasyon:** Projenin mimari detayları ve geliştirme günlüğü için ana dizindeki `Fin101_Technical_Doc.md` dosyası incelenebilir.
