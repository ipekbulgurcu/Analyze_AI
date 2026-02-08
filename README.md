# Local LLM Document Q&A (RAG) Service

**Yinov AI - Document Assistant**, yerel LLM (Ollama) kullanarak yüklenen PDF ve TXT dokümanları üzerinden soru cevaplayan, gizlilik odaklı ve yüksek performanslı bir RAG (Retrieval-Augmented Generation) servisidir.

## 🚀 Proje Hakkında
Bu proje, modern yapay zeka teknolojilerini (LLM, Vector Search) kullanarak kurumsal veya kişisel dokümanların analiz edilmesini sağlar. Verileriniz tamamen **yerel makinenizde** işlenir ve saklanır, herhangi bir bulut servisine gönderilmez.

### Öne Çıkan Özellikler
*   **Tamamen Yerel:** Ollama ile Mistral, Llama 3 veya GPT-OSS modellerini internet olmadan çalıştırır.
*   **Modern Arayüz:** Google Material Design 3 prensiplerine uygun, kullanıcı dostu web arayüzü.
*   **Hızlı ve Güvenli:** FastAPI ile asenkron API yapısı ve ChromaDB ile vektör tabanlı hızlı arama.
*   **Clean Architecture:** Modüler, test edilebilir ve genişletilebilir kod yapısı.

## 🛠️ Kurulum Adımları

Projeyi çalıştırmak için aşağıdaki adımları takip edin.

### 1. Ön Gereksinimler
*   **Python 3.10+**: Sisteminizde Python yüklü olmalıdır.
*   **Ollama**: Yerel LLM servisi. [ollama.com](https://ollama.com) adresinden indirin.

### 2. Projeyi Klonlama
```bash
git clone https://github.com/username/local_rag_service.git
cd local_rag_service
```

### 3. Sanal Ortam (Virtual Environment) Kurulumu
```bash
# Windows için
python -m venv venv
venv\Scripts\activate

# Linux/Mac için
python3 -m venv venv
source venv/bin/activate
```

### 4. Bağğımlılıkların Yüklenmesi
```bash
pip install -r requirements.txt
```

### 5. LLM Modelinin İndirilmesi
Terminalde şu komutu çalıştırarak kullanacağınız modeli indirin (Örn: mistral):
```bash
ollama pull mistral
```
*(Not: Farklı bir model kullanacaksanız `app/core/config.py` dosyasındaki `LLM_MODEL` ayarını güncelleyin.)*

### 6. Uygulamanın Çalıştırılması
Ollama servisinin arka planda çalıştığından emin olun, ardından:
```bash
uvicorn app.main:app --reload
```
Uygulamanız **http://127.0.0.1:8000** adresinde yayında olacaktır.

## 🏗️ Teknoloji Seçimi ve Gerekçelendirme

Projenin mimarisinde kullanılan teknolojiler, performans ve sürdürülebilirlik gözetilerek seçilmiştir:

| Teknoloji | Seçim Nedeni |
| :--- | :--- |
| **FastAPI** | Python ekosistemindeki en hızlı web framework'lerinden biridir. Asenkron (async/await) yapısı sayesinde yüksek eşzamanlı istekleri (concurrency) verimli yönetir ve otomatik Swagger dokümantasyonu sunar. |
| **ChromaDB** | Açık kaynaklı, yerel çalışabilen ve kurulumu kolay bir vektör veritabanıdır. Doküman gömülerini (embeddings) hızlıca saklar ve "Semantic Search" (anlamsal arama) için optimize edilmiştir. |
| **LangChain** | LLM uygulamaları geliştirmek için endüstri standardı bir orkestrasyon kütüphanesidir. Doküman yükleme, parçalama (chunking) ve LLM ile iletişim süreçlerini standardize eder. |
| **Ollama** | Llama 3, Mistral gibi güçlü modelleri yerel makinede (CPU/GPU) çalıştırmayı sağlayan en pratik çözümdür. Docker benzeri yapısıyla model yönetimini kolaylaştırır. |
| **Pydantic** | Veri doğrulama (data validation) ve ayar yönetimi için kullanıldı. Tip güvenliği (type safety) sağlayarak çalışma zamanı hatalarını minimize eder. |

## 🧪 Testler
Birim testlerini çalıştırmak için:
```bash
pytest tests/
```

---
**Geliştirici:** İpek Bulgurcu
**Lisans:** MIT
