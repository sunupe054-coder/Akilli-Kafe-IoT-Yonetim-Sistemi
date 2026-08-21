import pyodbc
import time
import random

def baglanti_al():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=.\\SQLEXPRESS;'
        'DATABASE=AkilliKafeDB;'
        'Trusted_Connection=yes;'
    )

print("🚀 Akıllı Kafe Canlı Simülatörü Başlatıldı...")
print("Sensörler, Mutfak ve Masa Operasyonları devrede...\n")

while True:
    try:
        conn = baglanti_al()
        cursor = conn.cursor()

        # ==========================================
        # 1. IOT LAVABO SENSÖR SİMÜLASYONU
        # ==========================================
        cursor.execute("SELECT * FROM LavaboDurumu")
        satirlar = cursor.fetchall()
        if satirlar:
            secilen = random.choice(satirlar)
            lavabo_id = secilen[0]
            kat_adi = secilen[1]
            yeni_durum_bit = random.choice([0, 1])
            
            kolon_adi = cursor.description[2][0]
            id_kolon_adi = cursor.description[0][0]
            
            cursor.execute(f"UPDATE LavaboDurumu SET {kolon_adi} = ? WHERE {id_kolon_adi} = ?", (yeni_durum_bit, lavabo_id))
            conn.commit()
            simge = "🔴" if yeni_durum_bit == 1 else "🟢"
            print(f"[{time.strftime('%H:%M:%S')}] 🚽 Sensör: {kat_adi} -> {simge}")

        # ==========================================
        # 2. MUTFAK SİPARİŞ DURUMU AKIŞI
        # ==========================================
        cursor.execute("SELECT TOP 1 SiparisID, SiparisDurumu, MasaID FROM Siparisler WHERE SiparisDurumu IN ('Hazirlaniyor', 'Hazırlanıyor', 'Hazirlandi', 'Hazırlandı') ORDER BY NEWID()")
        siparis = cursor.fetchone()

        if siparis:
            siparis_id = siparis[0]
            mevcut_durum = str(siparis[1])
            masa_id = siparis[2]

            # Hazırlanıyor -> Hazırlandı -> Tamamlandı geçişi
            if "Hazirlan" in mevcut_durum or "Hazırlan" in mevcut_durum:
                yeni_durum = "Hazırlandı"
                print(f"[{time.strftime('%H:%M:%S')}] 🍳 Mutfak: Sipariş #{siparis_id} -> {yeni_durum}")
            else:
                yeni_durum = "Tamamlandı"
                print(f"[{time.strftime('%H:%M:%S')}] ✅ Servis: Sipariş #{siparis_id} -> {yeni_durum}")

            cursor.execute("UPDATE Siparisler SET SiparisDurumu = ? WHERE SiparisID = ?", (yeni_durum, siparis_id))
            conn.commit()

        # ==========================================
        # 3. ÖDEME ALMA VE MASA BOŞALTMA SİMÜLASYONU
        # ==========================================
        # Tamamlanan siparişi olan dolu bir masayı bul ve ödemesini alıp masayı 'Boş' yap
        cursor.execute("""
            SELECT TOP 1 m.MasaID, m.MasaNo 
            FROM Masalar m
            JOIN Siparisler s ON m.MasaID = s.MasaID
            WHERE (m.Durum = 'Dolu' OR m.Durum = 'DOLU') 
              AND s.SiparisDurumu = 'Tamamlandı'
            ORDER BY NEWID()
        """)
        dolu_masa = cursor.fetchone()

        if dolu_masa:
            bosalacak_masa_id = dolu_masa[0]
            bosalacak_masa_no = dolu_masa[1]
            
            # Masayı boşalt
            cursor.execute("UPDATE Masalar SET Durum = 'Boş' WHERE MasaID = ?", (bosalacak_masa_id,))
            conn.commit()
            print(f"[{time.strftime('%H:%M:%S')}] 💳 Ödeme Alındı: {bosalacak_masa_no} hesabı ödedi, masa BOŞALTILDI.")

        conn.close()
        time.sleep(10)

    except Exception as e:
        print(f"Hata oluştu: {e}")
        time.sleep(5)