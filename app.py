import streamlit as st
import pyodbc
import time

# Sayfa genel ayarları
st.set_page_config(page_title="Akıllı Kafe ve Mutfak", page_icon="☕", layout="wide")

# Otomatik Yenileme (Sayfa her 5 saniyede bir arka planda veritabanından güncellenir)
st_autorefresh_js = """
<script>
    setTimeout(function() {
        window.location.reload();
    }, 5000);
</script>
"""

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

# Veritabanı bağlantısı
def baglanti_al():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=.\\SQLEXPRESS;'
        'DATABASE=AkilliKafeDB;'
        'Trusted_Connection=yes;'
    )

# Sol Menü
st.sidebar.title("☕ Menü")
ekran_secimi = st.sidebar.radio("Mod Seçiniz:", ["📱 Müşteri Ekranı", "👨‍🍳 Yönetici & Mutfak Paneli"])

# Otomatik Canlı Takip Aç/Kapa
canli_takip = st.sidebar.toggle("📡 Canlı Veri Akışı (Oto-Yenileme)", value=True)

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

    # Canlı Lavabo Durumları
    try:
        conn = baglanti_al()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LavaboDurumu")
        lavabolar = cursor.fetchall()
        conn.close()

        if lavabolar:
            col_l1, col_l2 = st.columns(len(lavabolar))
            for i, lavabo in enumerate(lavabolar):
                kat = str(lavabo[1])
                durum = str(lavabo[2]).strip()
                if durum in ["1", "True", "Dolu", "DOLU", "dolu"]:
                    durum_metni = "🔴 Dolu"
                    stil = "lavabo-dolu"
                else:
                    durum_metni = "🟢 Boş"
                    stil = "lavabo-bos"
                
                with col_l1 if i == 0 else col_l2:
                    st.markdown(f'<div class="lavabo-kutu {stil}">{kat} | {durum_metni}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Lavabo verisi alınamadı: {e}")

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
        try:
            conn = baglanti_al()
            cursor = conn.cursor()
            cursor.execute("SELECT MasaID, MasaNo FROM Masalar WHERE Durum NOT IN ('Dolu', 'dolu', 'DOLU', '1') OR Durum IS NULL")
            masalar = cursor.fetchall()
            masa_dict = {str(m[1]): m[0] for m in masalar}

            cursor.execute("SELECT KategoriID, KategoriAdi FROM Kategoriler")
            kategoriler = cursor.fetchall()
            kategori_dict = {str(k[1]): k[0] for k in kategoriler}

            cursor.execute("SELECT UrunID, UrunAdi, KategoriID, Fiyat FROM Urunler ORDER BY UrunAdi ASC")
            tum_urunler = cursor.fetchall()
            conn.close()
        except:
            masa_dict, kategori_dict, tum_urunler = {}, {}, []

        if not masa_dict:
            st.warning("⚠️ Şu anda tüm masalar dolu görünüyor.")
        else:
            secilen_masa = st.selectbox("Masa Seçiniz:", list(masa_dict.keys()), key="siparis_masa")
            secilen_kategori = st.selectbox("Kategori Seçiniz:", list(kategori_dict.keys()), key="siparis_kat")

            kat_id = kategori_dict.get(secilen_kategori)
            filtrelenmis = {str(u[1]): {"id": u[0], "fiyat": float(u[3])} for u in tum_urunler if u[2] == kat_id}

            secilen_urun = st.selectbox("Ürün Seçiniz:", list(filtrelenmis.keys()), key="siparis_urun")
            adet = st.number_input("Adet:", min_value=1, max_value=10, value=1)
            siparis_notu = st.text_input("Sipariş Notunuz:", placeholder="Örn: Yulaf sütlü olsun / Az pişmiş olsun...", key="siparis_not")

            # Tavsiye Motoru
            oneri_urun_adi = None
            oneri_mesaj = ""
            urun_kucuk = secilen_urun.lower()

            if any(t in urun_kucuk for t in ["cheesecake", "sufle", "trileçe", "tatlı", "tiramisu", "brownie", "profiterol", "kruvasan"]):
                if "kruvasan" in urun_kucuk:
                    oneri_urun_adi = "Filtre Kahve"
                    oneri_mesaj = "Taze kruvasan yanına nefis bir Filtre Kahve!"
                else:
                    oneri_urun_adi = "Demleme Bardak Çay"
                    oneri_mesaj = "Tatlı yanına taze demlenmiş tavşan kanı çay!"

            elif any(y in urun_kucuk for y in ["burger", "makarna", "penne", "spagetti", "köfte", "wrap", "dürüm", "sepet"]):
                if "burger" in urun_kucuk or "sepet" in urun_kucuk:
                    oneri_urun_adi = "Kola (Kutu 330ml)"
                    oneri_mesaj = "Yemeğinizin yanına buz gibi bir kutu kola!"
                elif "köfte" in urun_kucuk or "wrap" in urun_kucuk:
                    oneri_urun_adi = "Ev Yapımı Köy Ayranı"
                    oneri_mesaj = "Dürüm/Köfte yanına ferahlatıcı yayık ayranı!"
                else:
                    oneri_urun_adi = "Ice Tea Şeftali"
                    oneri_mesaj = "Makarnanızın yanına ferahlatıcı soğuk çay!"

            elif "salata" in urun_kucuk:
                oneri_urun_adi = "Maden Suyu / Soda"
                oneri_mesaj = "Sağlıklı salata yanına ferahlatıcı maden suyu!"

            elif any(k in urun_kucuk for k in ["latte", "mocha", "cappuccino", "macchiato", "kahve", "americano", "cold brew"]):
                if "iced" in urun_kucuk or "cold" in urun_kucuk:
                    oneri_urun_adi = "Çikolatalı Ilık Brownie"
                    oneri_mesaj = "Soğuk kahve yanına sıcacık çikolatalı brownie!"
                else:
                    oneri_urun_adi = "San Sebastian Cheesecake"
                    oneri_mesaj = "Kahve yanına meşhur San Sebastian Cheesecake!"

            else:
                oneri_urun_adi = "Çikolatalı Islak Sufle & Dondurma"
                oneri_mesaj = "İçeceğinizin yanına nefis dondurmalı bir sufle!"

            oneri_obj = next((u for u in tum_urunler if u[1] == oneri_urun_adi), None)
            oneri_eklendi = False

            if oneri_obj:
                normal_fiyat = float(oneri_obj[3])
                indirimli_fiyat = normal_fiyat * 0.90

                st.markdown(f"""
                <div class="oneri-kutusu">
                    💡 <b>Şefin Akıllı Tavsiyesi:</b> {oneri_mesaj}<br>
                    🎁 <b>Özel İndirimli Eşleşme:</b> {oneri_obj[1]} &nbsp; 
                    <s>{normal_fiyat:.2f} TL</s> ➔ <b>{indirimli_fiyat:.2f} TL (%10 İndirim)</b>
                </div>
                """, unsafe_allow_html=True)
                oneri_eklendi = st.checkbox(f"Tavsiye Edilen Ürünü İndirimli Ekle: {oneri_obj[1]} (+{indirimli_fiyat:.2f} TL)", value=False)

            birim_fiyat = filtrelenmis[secilen_urun]["fiyat"]
            urun_id = filtrelenmis[secilen_urun]["id"]
            toplam_tutar = birim_fiyat * adet

            if oneri_eklendi and oneri_obj:
                toplam_tutar += indirimli_fiyat

            st.markdown(f'<div class="fiyat-alani">☕ Toplam Tutar: {toplam_tutar:.2f} TL</div>', unsafe_allow_html=True)

            if st.button("Siparişi Onayla ☕", key="btn_siparis_onayla"):
                conn = baglanti_al()
                cursor = conn.cursor()
                masa_id = masa_dict[secilen_masa]
                cursor.execute("INSERT INTO Siparisler (MasaID, MusteriNotu) VALUES (?, ?)", (masa_id, siparis_notu))
                conn.commit()

                cursor.execute("SELECT MAX(SiparisID) FROM Siparisler")
                siparis_id = int(cursor.fetchone()[0])
                
                cursor.execute("INSERT INTO SiparisDetay (SiparisID, UrunID, Adet, BirimFiyat) VALUES (?, ?, ?, ?)",
                               (siparis_id, urun_id, adet, birim_fiyat))
                
                if oneri_eklendi and oneri_obj:
                    cursor.execute("INSERT INTO SiparisDetay (SiparisID, UrunID, Adet, BirimFiyat) VALUES (?, ?, ?, ?)",
                                   (siparis_id, oneri_obj[0], 1, indirimli_fiyat))
                    
                    sorumlu_personel = masa_garson_eslesme.get(secilen_masa, "Genel Servis")
                    cursor.execute("""
                        INSERT INTO PersonelPrim (PersonelAdi, MasaNo, TavsiyeUrun, PrimTutari)
                        VALUES (?, ?, ?, ?)
                    """, (sorumlu_personel, secilen_masa, oneri_obj[1], 15.0))

                cursor.execute("UPDATE Masalar SET Durum = 'Dolu' WHERE MasaID = ?", (masa_id,))
                conn.commit()
                conn.close()
                st.success("✅ Siparişiniz başarıyla iletildi!")
                st.rerun()

    # SEKME 2: GARSON ÇAĞIR
    with tab2:
        try:
            conn = baglanti_al()
            cursor = conn.cursor()
            cursor.execute("SELECT MasaID, MasaNo FROM Masalar")
            tum_m = cursor.fetchall()
            conn.close()
            tum_masalar_dict = {str(m[1]): m[0] for m in tum_m}
        except:
            tum_masalar_dict = {}

        talep_masasi = st.selectbox("Hangi Masadasınız?", list(tum_masalar_dict.keys()), key="garson_masa")
        talep_turu = st.selectbox("İhtiyacınızı Seçin:", [
            "🍴 Çatal / Kaşık / Bıçak", 
            "🧻 Peçete / Islak Mendil", 
            "🧂 Ketçap / Mayonez / Sos", 
            "💧 Su / Ekstra Bardak / Buz", 
            "💳 Hesap / POS Cihazı", 
            "🙋 Garson Çağır", 
            "✏️ Diğer İhtiyaç"
        ])
        talep_notu = st.text_input("Açıklama:", placeholder="Örn: Ekstra bardak rica ediyoruz...", key="garson_not")

        if st.button("İsteği Personele İlet 🚀", key="btn_talep_ilet"):
            if talep_masasi:
                conn = baglanti_al()
                cursor = conn.cursor()
                m_id = tum_masalar_dict[talep_masasi]
                cursor.execute("INSERT INTO MasaTalepleri (MasaID, TalepTuru, Aciklama) VALUES (?, ?, ?)", (m_id, talep_turu, talep_notu))
                conn.commit()
                conn.close()
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
        conn = baglanti_al()
        cursor = conn.cursor()

        cursor.execute("SELECT ISNULL(SUM(Adet * BirimFiyat), 0) FROM SiparisDetay")
        toplam_ciro = float(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM Masalar WHERE Durum IN ('Dolu', 'dolu', 'DOLU', '1')")
        dolu_masa_sayisi = int(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM Masalar")
        toplam_masa_sayisi = int(cursor.fetchone()[0])

        cursor.execute("SELECT ISNULL(SUM(PrimTutari), 0) FROM PersonelPrim")
        toplam_dagitilan_prim = float(cursor.fetchone()[0])

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("💰 Toplam Ciro", f"{toplam_ciro:.2f} TL")
        kpi2.metric("🪑 Masa Doluluk Oranı", f"{dolu_masa_sayisi} / {toplam_masa_sayisi} Masa")
        kpi3.metric("🎁 Dağıtılan Satış Primi", f"{toplam_dagitilan_prim:.2f} TL")

        st.write("---")

        col_sol, col_sag = st.columns([1.1, 0.9])

        with col_sol:
            st.subheader("👨‍🍳 Mutfak Sipariş Akışı")
            cursor.execute("""
                SELECT s.SiparisID, m.MasaNo, u.UrunAdi, sd.Adet, (sd.Adet * sd.BirimFiyat) as Tutar, s.MusteriNotu
                FROM Siparisler s
                JOIN Masalar m ON s.MasaID = m.MasaID
                JOIN SiparisDetay sd ON s.SiparisID = sd.SiparisID
                JOIN Urunler u ON sd.UrunID = u.UrunID
                ORDER BY s.SiparisID DESC
            """)
            gelen_siparisler = cursor.fetchall()

            if gelen_siparisler:
                for sip in gelen_siparisler[:8]:
                    not_bilgisi = f" (Not: {sip[5]})" if sip[5] else ""
                    st.markdown(f"""
                    <div class="siparis-karti">
                        <b>📍 {sip[1]}</b> — ☕ {sip[2]} (x{sip[3]}) <b>[{sip[4]:.2f} TL]</b>{not_bilgisi}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Henüz bekleyen sipariş bulunmuyor.")

        with col_sag:
            st.subheader("🏆 Personel Satış & Prim Başarısı")
            cursor.execute("""
                SELECT PersonelAdi, COUNT(*) as SatisSayisi, SUM(PrimTutari) as ToplamPrim
                FROM PersonelPrim
                GROUP BY PersonelAdi
                ORDER BY ToplamPrim DESC
            """)
            primler = cursor.fetchall()

            if primler:
                for p in primler:
                    st.markdown(f"""
                    <div class="prim-karti">
                        🥇 <b>{p[0]}</b>: <b>{p[1]} Adet</b> Tavsiye Satışı ➔ <b>+{float(p[2]):.2f} TL Prim</b>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("Henüz tavsiye üzerinden gerçekleşen primli satış bulunmuyor.")

            st.write("---")
            st.subheader("💳 Masa / Hesap Sıfırlama")
            cursor.execute("SELECT MasaID, MasaNo FROM Masalar WHERE Durum IN ('Dolu', 'dolu', 'DOLU', '1')")
            dolu_masalar = cursor.fetchall()

            if dolu_masalar:
                secilen_kapatilacak = st.selectbox("Hesabı Kapanan Masa:", [m[1] for m in dolu_masalar], key="kapat_masa")
                if st.button("Masayı Boşalt / Sıfırla 🟢", key="btn_masa_bosalt"):
                    cursor.execute("UPDATE Masalar SET Durum = 'Boş' WHERE MasaNo = ?", (secilen_kapatilacak,))
                    conn.commit()
                    st.success(f"{secilen_kapatilacak} başarıyla 'Boş' duruma getirildi.")
                    conn.close()
                    st.rerun()
            else:
                st.success("Tüm masalar şu anda boş durumda.")

        conn.close()

# Sayfanın en altına otomatik 5 saniyede bir yenileme tetikleyicisi
if canli_takip:
    time.sleep(5)
    st.rerun()