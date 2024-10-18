import subprocess
import sys

# Dosya yolu
resolv_conf_path = "/etc/resolv.conf"

# Yeni DNS ayarları
new_dns = """# Generated by NetworkManager
#nameserver 192.168.1.1
nameserver 8.8.8.8
nameserver 8.8.4.4
"""

# DNS sunucuları listesi
dns_listesi = {
    "Level3": "209.244.0.3 - 209.244.0.4",
    "OpenDNS": "208.67.222.222 - 208.67.220.220",
    "Google": "8.8.8.8 - 8.8.4.4",
    "Verisign": "64.6.64.6 - 64.6.65.6",
    "DNS.WATCH": "84.200.69.80 - 84.200.70.40",
    "Comodo": "8.26.56.26 - 8.20.247.20",
    "DNS Advantage (UltraDns)": "156.154.70.1 - 156.154.71.1",
    "SafeDNS": "195.46.39.39 - 195.46.39.40",
    "openNIC": "96.90.175.167 - 193.183.98.154",
    "DynDNS": "216.146.35.35 - 216.146.36.36",
    "Alternate": "198.101.242.72 - 23.253.163.53",
    "Yandex": "77.88.8.8 - 77.88.8.1",
    "TTnet (Türk Telekom)": "195.175.39.49 - 195.175.39.50"
}

# Yardım dökümanı
def help_dokumani():
    print("""
Kullanım: python3 script_name.py [seçenekler]

Seçenekler:
  -h, --help      Yardım dökümanını gösterir.
  -list           Mevcut DNS sunucularının listesini gösterir.
  -change         DNS ayarlarını otomatik olarak Google DNS ile değiştirir.
  -dns            Mevcut DNS Gösterir.
""")

# Yazma iznini kaldırma
def yazma_iznini_kaldir():
    try:
        subprocess.run(["sudo", "chattr", "-i", resolv_conf_path], check=True)
    except subprocess.CalledProcessError:
        # Eğer yazma izni kalkmazsa '-a' parametresi ile tekrar deniyoruz.
        subprocess.run(["sudo", "chattr", "-a", resolv_conf_path], check=True)

# DNS ayarlarını değiştirme
def dns_ayarlari_degistir():
    try:
        with open(resolv_conf_path, 'w') as dosya:
            dosya.write(new_dns)
        print("DNS ayarları başarıyla değiştirildi.")
    except Exception as e:
        print(f"Hata: {e}")

# Yazma iznini geri alma
def yazma_iznini_geri_al():
    subprocess.run(["sudo", "chattr", "+i", resolv_conf_path], check=True)

# DNS sunucu listesini gösterme
def dns_listesini_goster():
    print("Mevcut DNS Sunucuları Listesi:")
    for isim, adres in dns_listesi.items():
        print(f"{isim}:  {adres}")

# mevcut dns gösterme
def mevcut_dns():
    subprocess.run(["cat", resolv_conf_path], check=True)

# Ana fonksiyon
def main():
    if len(sys.argv) < 2:
        print("Lütfen bir seçenek belirtin. Yardım için -h seçeneğini kullanın.")
        return

    secenek = sys.argv[1]

    if secenek in ("-h", "--help"):
        help_dokumani()
    elif secenek == "-list":
        dns_listesini_goster()
    elif secenek == "-change":
        yazma_iznini_kaldir()
        dns_ayarlari_degistir()
        yazma_iznini_geri_al()
    elif secenek == "-dns":
        mevcut_dns()    
    else:
        print("Bilinmeyen seçenek. Yardım için -h seçeneğini kullanın.")

if __name__ == "__main__":
    main()
