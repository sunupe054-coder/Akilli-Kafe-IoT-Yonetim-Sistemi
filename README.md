# ☕ Akıllı Kafe Yönetim ve IoT Tabanlı Karar Destek Sistemi

Uçtan uca geliştirilmiş bu proje; kafe ve restoran işletmelerinde müşteri sipariş süreçlerini, mutfak operasyonlarını, IoT sensör tabanlı ortam durumlarını (lavabo/doluluk) ve yönetici iş zekası analitiğini tek bir entegre mimaride birleştiren akıllı bir yönetim sistemidir.

---

### 📱 Canlı Demo (Prototip)
Müşteri sipariş ekranını anında deneyimlemek için aşağıdaki QR kodu telefonunuzla taratabilirsiniz:

<p align="center">
  <img src="AkıllıKafe_QR.png" width="220" alt="Sipariş Ekranı QR Kodu">
</p>

*(Not: Tarattığınızda doğrudan `sunupe054-coder-yeni.streamlit.app` canlı sipariş arayüzüne yönlendirilirsiniz).*

---

## 🚀 Proje Mimarisi ve Kullanılan Teknolojiler

* **Veritabanı Katmanı (Database):** Microsoft SQL Server (İlişkisel Veritabanı Mimarisi, Tablolar, İlişkiler, Stored Procedures, Views)
* **Kullanıcı & Operasyon Arayüzü:** Python & Streamlit (Müşteri Sipariş Ekranı, Canlı Mutfak Paneli, Yönetici Masası Sıfırlama)
* **IoT & Sensör Simülatörü:** Python (Arka planda gerçek zamanlı lavabo doluluk ve cihaz durumlarını simüle eden thread tabanlı veri üretici)
* **İş Zekası & Analitik (Business Intelligence):** Microsoft Power BI (Anlık ciro, sipariş yoğunluğu, popüler ürünler ve doluluk oranları gösterge paneli)
* **Sürücü / Entegrasyon:** `pyodbc`

---

## 📌 Temel Özellikler

1. **Müşteri Sipariş Modülü:**
   * Dinamik kategori ve ürün listeleme,
   * Görsel vitrin tasarımı ve kullanıcı dostu arayüz,
   * Özel sipariş notu ve garson çağırma talepleri.

2. **Mutfak & Operasyon Paneli:**
   * Gelen siparişlerin durum bazlı anlık akışı (`Hazırlanıyor`, `Hazırlandı`),
   * Masa hesabı kapatma ve masa durumunu otomatik güncelleme.

3. **IoT Sensör İzleme:**
   * Kat bazlı lavabo doluluk durumlarının eşzamanlı takibi ve görselleştirilmesi.

4. **Power BI Yönetici Dashboard'u:**
   * Gerçek zamanlı veri akışı üzerinden satış trendleri ve operasyonel verimlilik analitiği.

---

## 🛠️ Kurulum ve Çalıştırma

1. **Gerekli Kütüphanelerin Yüklenmesi:**
   ```bash
   pip install streamlit pyodbc
