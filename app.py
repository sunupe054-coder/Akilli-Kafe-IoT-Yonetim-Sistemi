import streamlit as st
import random
import time

# Sayfa genel ayarları
st.set_page_config(page_title="Akıllı Kafe ve Mutfak", page_icon="☕", layout="wide")

# URL'den masa bilgisini otomatik yakalama (QR Kod Entegrasyonu)
query_params = st.query_params
qr_masa = query_params.get("masa", None)

# Şeffaf kafe teması ve estetik CSS
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: url("https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=1920&q=80") no-repeat center center fixed;
        background-size: cover;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.35);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 30px 24px;
        margin-top: 15px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    h1, h2, h3, label, p, span {
        color: #2b1408 !important;
        font-weight: bold;
    }
    .lavabo-kutu {
        padding: 12px 16px;
        border-radius: 14px;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 10px;
    }
    .lavabo-bos {
        background-color: rgba(212, 244, 221, 0.9);
        color: #0d5a2b !important;
        border: 1px solid #95d5a6;
    }
    .lavabo-dolu {
        background-color: rgba(253, 226, 228, 0.9);
        color: #842029 !important;
        border: 1px solid #f5b5ba;
    }
    .fiyat-alani {
        background: rgba(255, 255, 255, 0.65);
        border-left: 5px solid #c86432;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 12px 0;
        font-size: 1.05rem;
        font-weight: bold;
        color: #2b1408;
    }
    .oneri-kutusu {
        background: rgba(255, 243, 205, 0.92);
        border: 1.5px solid #ffeeba;
        border-left: 6px solid #e09f1a;
        border-radius: 14px;
        padding: 14px 18px;
        margin: 14px 0;
        color: #856404;
    }
    .siparis-karti {
        background: rgba(255, 255, 255, 0.65);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    .prim-karti {
        background: rgba(230, 244, 234, 0.85);
        border: 1px solid #c3e6cb;
        border-left: 5px solid #28a745;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
        font-size: 0.95rem;
    }
    .stButton > button {
        background-color: #c86432;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1rem;
        width: 100%;
        border: none;
        padding: 10px;
    }
    .stButton > button:hover {
        background-color: #a84e20;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sol Menü
st.sidebar.title("☕ Menü")
ekran_secimi = st.sidebar.radio("Mod Seçiniz:", ["📱 Müşteri Ekranı", "👨‍🍳 Yönetici & Mutfak Paneli"])

# Masa - Garson Arka Plan Eşleşmesi
masa_garson_eslesme = {
    "Masa 1": "Ahmet Yılmaz",
    "Masa 2": "Elif Kaya",
    "Masa 3": "Mehmet Demir",
    "Masa 4": "Selin Öztürk"
}

# ==========================================================
# 1. MOD: MÜŞTERİ EKRANI
# ==========================================================
if ekran_secimi == "📱 Müşteri Ekranı":
    st.title("☕ Akıllı Kafe ve Mutfak")

    # Dinamik Lavabo Durumu Simülasyonu (Ağ hatası vermez, canlı hissettirir)
    l1_durum = random.choice(["🟢 Boş", "🟢 Boş", "🔴 Dolu"])
    l2_durum = random.choice(["🟢 Boş", "🔴 Dolu", "🟢 Boş"])

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        stil_1 = "lavabo-bos" if "Boş" in l1_durum else "lavabo-dolu"
        st.markdown(f'<div class="lavabo-kutu {stil_1}">1. Kat Lavabo | {l1_durum}</div>', unsafe_allow_html=True)

    with col_l2:
        stil_2 = "lavabo-bos" if "Boş" in l2_durum else "lavabo-dolu"
        st.markdown(f'<div class="lavabo-kutu {stil_2}">2. Kat Lavabo | {l2_durum}</div>', unsafe_allow_html=True)

    st.write("")

    # Vitrin Görselleri
    col_vitrin = st.columns(3)
    with col_vitrin[0]:
        st.image("https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=400&q=80", caption="☕ Sıcak İçecekler")
    with col_vitrin[1]:
        st.image("https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=400&q=80", caption="🧊 Soğuk İçecekler")
    with col_vitrin[2]:
        st.image("https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=400&q=80", caption="🍰 Yiyecek, Salata & Tatlı")

    tab1, tab2 = st.tabs(["🍽️ Sipariş Ver", "🔔 Garson / İhtiyaç Çağır"])

    # SEKME 1: SİPARİŞ
    with tab1:
        masa_dict = {"Masa 1": 1, "Masa 2": 2, "Masa 3": 3, "Masa 4": 4}
        kategori_dict = {"Sıcak İçecekler": 1, "Soğuk İçecekler": 2, "Tatlılar": 3, "Yiyecekler": 4}
        tum_urunler = [
            (1, "Filtre Kahve", 1, 60.0),
            (2, "Türk Kahvesi", 1, 50.0),
            (3, "San Sebastian Cheesecake", 3, 120.0),
            (4, "Kruvasan", 4, 80.0),
            (5, "Hamburger Menü", 4, 180.0),
            (6, "Demleme Bardak Çay", 1, 25.0)
        ]

        if qr_masa and qr_masa in masa_dict:
            secilen_masa = qr_masa
            st.info(f"📍 **{qr_masa}** QR kodu ile bağlandınız.")
        else:
            secilen_masa = st.selectbox("Masa Seçiniz:", list(masa_dict.keys()), key="siparis_masa")

        secilen_kategori = st.selectbox("Kategori Seçiniz:", list(kategori_dict.keys()), key="siparis_kat")
        kat_id = kategori_dict.get(secilen_kategori)
        filtrelenmis = {str(u[1]): {"id": u[0], "fiyat": float(u[3])} for u in tum_urunler if u[2] == kat_id}

        if not filtrelenmis:
            filtrelenmis = {str(u[1]): {"id": u[0], "fiyat": float(u[3])} for u in tum_urunler}

        secilen_urun = st.selectbox("Ürün Seçiniz:", list(filtrelenmis.keys()), key="siparis_urun")
        adet = st.number_input("Adet:", min_value=1, max_value=10, value=1)
        siparis_notu = st.text_input("Sipariş Notunuz:", placeholder="Örn: Yulaf sütlü olsun...", key="siparis_not")

        # Tavsiye Motoru
        oneri_urun_adi = "San Sebastian Cheesecake"
        oneri_mesaj = "Kahvenizin yanına nefis bir San Sebastian Cheesecake!"
        
        oneri_obj = next((u for u in tum_urunler if u[1] == oneri_urun_adi), tum_urunler[0])
        normal_fiyat = float(oneri_obj[3])
        indirimli_fiyat = normal_fiyat * 0.90

        st.markdown(f"""
        <div class="oneri-kutusu">
            💡 <b>Şefin Akıllı Tavsiyesi:</b> {oneri_mesaj}<br>
            🎁 <b>Özel İndirimli Eşleşme:</b> {oneri_obj[1]} &nbsp; 
            <s>{normal_fiyat:.2f} TL</s> ➔ <b>{indirimli_fiyat:.2f} TL (%10 İndirim)</b>
        </div>
        """, unsafe_allow_html=True)
        oneri_eklendi = st.checkbox(f"Tavsiye Edilen Ürünü İndirimli Ekle (+{indirimli_fiyat:.2f} TL)", value=False)

        birim_fiyat = filtrelenmis[secilen_urun]["fiyat"]
        toplam_tutar = birim_fiyat * adet
        if oneri_eklendi:
            toplam_tutar += indirimli_fiyat

        st.markdown(f'<div class="fiyat-alani">☕ Toplam Tutar: {toplam_tutar:.2f} TL</div>', unsafe_allow_html=True)

        if st.button("Siparişi Onayla ☕", key="btn_siparis_onayla"):
            st.success("✅ Siparişiniz başarıyla alındı!")

    # SEKME 2: GARSON ÇAĞIR
    with tab2:
        talep_masasi = st.selectbox("Hangi Masadasınız?", list(masa_dict.keys()), key="garson_masa")
        talep_turu = st.selectbox("İhtiyacınızı Seçin:", [
            "🍴 Çatal / Kaşık / Bıçak", 
            "🧻 Peçete / Islak Mendil", 
            "🧂 Ketçap / Mayonez / Sos", 
            "💧 Su / Ekstra Bardak / Buz", 
            "💳 Hesap / POS Cihazı", 
            "🙋 Garson Çağır"
        ])
        talep_notu = st.text_input("Açıklama:", placeholder="Ekstra talebiniz var mı?", key="garson_not")

        if st.button("İsteği Personele İlet 🚀", key="btn_talep_ilet"):
            st.success(f"🔔 Talebiniz personele iletildi! ({talep_masasi} - {talep_turu})")

# ==========================================================
# 2. MOD: YÖNETİCİ & MUTFAK KARAR DESTEK PANELİ
# ==========================================================
else:
    st.title("📊 Yönetici & Mutfak Karar Destek Paneli")
    pin = st.sidebar.text_input("Yönetici PIN Kodu:", type="password", value="1234")
    if pin != "1234":
        st.warning("🔒 Lütfen sol menüden doğru PIN kodunu giriniz.")
    else:
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("💰 Toplam Ciro", "1,450.00 TL")
        kpi2.metric("🪑 Masa Doluluk Oranı", "2 / 4 Masa")
        kpi3.metric("🎁 Dağıtılan Satış Primi", "45.00 TL")

        st.write("---")
        col_sol, col_sag = st.columns([1.1, 0.9])

        with col_sol:
            st.subheader("👨‍🍳 Mutfak Sipariş Akışı")
            st.markdown("""
            <div class="siparis-karti"><b>📍 Masa 1</b> — ☕ Filtre Kahve (x2) <b>[120.00 TL]</b></div>
            <div class="siparis-karti"><b>📍 Masa 3</b> — 🍰 San Sebastian Cheesecake (x1) <b>[120.00 TL]</b></div>
            """, unsafe_allow_html=True)

        with col_sag:
            st.subheader("🏆 Personel Satış & Prim Başarısı")
            st.markdown("""
            <div class="prim-karti">🥇 <b>Ahmet Yılmaz</b>: <b>2 Adet</b> Tavsiye Satışı ➔ <b>+30.00 TL Prim</b></div>
            <div class="prim-karti">🥈 <b>Elif Kaya</b>: <b>1 Adet</b> Tavsiye Satışı ➔ <b>+15.00 TL Prim</b></div>
            """, unsafe_allow_html=True)
