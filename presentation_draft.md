# Teknik Sunum Taslağı: Local LLM Document Q&A Service

---

## Sayfa 1: Problem Tanımı
**Başlık:** Bilgiye Erişimde Hız ve Gizlilik İhtiyacı

**Metin:**
Günümüzde kurumlar ve bireyler, her gün artan miktarda dijital doküman (PDF, Raporlar, Sözleşmeler) ile çalışmaktadır. Bu dokümanların içinde aradığımız spesifik bilgiyi bulmak zaman alıcı ve verimsiz bir süreçtir.

Geleneksel "CTRL+F" (Kelime bazlı arama) yöntemleri, kullanıcının niyetini veya anlamsal bağlamı (context) anlayamaz.

**Mevcut Çözümlerin Kısıtları:**
*   **Bulut Tabanlı LLM'ler (OpenAI, Claude vb.):** Güçlüdür ancak kurumsal/hassas verilerin üçüncü parti sunuculara gönderilmesi gizlilik (Privacy) ve KVKK açısından risk oluşturur.
*   **Manuel İnceleme:** Yavaş, hataya açık ve ölçeklenemez.

**İhtiyaç:**
Dokümanları anlayan, sorulara doğal dilde cevap veren, ancak veriyi asla dışarı çıkarmayan **Yerel ve Akıllı** bir asistana ihtiyaç vardır.

---

## Sayfa 2: Çözüm Modülleri
**Başlık:** Yerel RAG Mimarisi ile Akıllı Doküman Analizi

**Metin:**
Geliştirdiğimiz çözüm, Retrieval-Augmented Generation (RAG) mimarisini kullanarak yerel kaynaklarla çalışan modüler bir sistemdir.

**Temel Bileşenler:**
1.  **API Katmanı (FastAPI):**
    *   Sistemin dış dünyaya açılan kapısıdır.
    *   Yüksek performanslı, asenkron ve RESTful mimariye sahiptir.
    *   Kullanıcı arayüzü ile backend arasındaki iletişimi yönetir.

2.  **Vektör Katmanı (ChromaDB + Embeddings):**
    *   Dokümanlar metin olarak değil, sayısal vektörler (embedding) olarak saklanır.
    *   Bu sayede kelime eşleşmesi değil, **kavramsal/anlamsal eşleşme** yapılır.
    *   Tamamen yerel disk üzerinde çalışır.

3.  **LLM Katmanı (Ollama):**
    *   `Mistral` veya `Llama 3` gibi açık kaynak modelleri çalıştırır.
    *   Vektör veritabanından gelen "alakalı bilgiyi" alıp, kullanıcıya anlamlı bir cevap üretir.

---

## Sayfa 3: Mimari Akış
**Başlık:** Sistem Nasıl Çalışıyor? (Workflow)

**Diyagram (Mermaid):**
```mermaid
graph TD
    User[Kullanıcı] -->|PDF Yükler| UI[Web Arayüzü]
    UI -->|/ingest POST| API[FastAPI Backend]
    API -->|Metni Çıkar| Loader[PDF Loader]
    Loader -->|Parçala (Chunking)| Splitter[Text Splitter]
    Splitter -->|Vektöre Çevir| Embed[Embedding Model]
    Embed -->|Kaydet| VectorDB[(ChromaDB)]
    
    User -->|Soru Sorar| UI
    UI -->|/ask POST| API
    API -->|Benzerlik Araması| VectorDB
    VectorDB -->|Alakalı Parçalar| API
    API -->|Soru + Context| LLM[Ollama (Local LLM)]
    LLM -->|Cevap| User
```

**Adım Adım Süreç:**
1.  **Ingestion (Veri Girişi):** Doküman yüklenir, küçük parçalara bölünür ve vektör veritabanına indekslenir.
2.  **Retrieval (Erişim):** Kullanıcı sorusuna en yakın doküman parçaları bulunur.
3.  **Generation (Üretim):** Bulunan parçalar ve soru LLM'e verilir, LLM nihai cevabı üretir.

---

## Sayfa 4: Literatür & Karşılaştırma
**Başlık:** Neden Bu Teknoloji Stack'i?

**Neden Yerel LLM?**
*   **Veri Gizliliği (Data Privacy):** Verileriniz internete çıkmaz, tamamen kendi donanımınızda işlenir. Finansal raporlar, hukuksal metinler için kritiktir.
*   **Maliyet (Cost):** OpenAI gibi servislerde token başına ücret ödenirken, yerel modelin maliyeti sadece donanım kaynağıdır (Elektrik/CPU).
*   **Bağımsızlık:** İnternet kesintisi veya servis sağlayıcı problemlerinden etkilenmez.

**RAG vs Fine-Tuning:**
*   Doküman analizi için **RAG (Retrieval-Augmented Generation)** tercih edilmiştir.
*   *Fine-Tuning* (Modeli eğitmek) pahalıdır ve modelin bilgisi eğitimi bittiği an eskir.
*   *RAG* ise, modele yeni bir dokümanı saniyeler içinde "öğretmenize" (context olarak vermenize) olanak tanır. Çok daha esnek ve günceldir.
