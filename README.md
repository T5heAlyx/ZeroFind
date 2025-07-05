# ZeroFind Zafiyet Tarama Aracı [ALPHA]

![version](https://img.shields.io/badge/version-2.0-blue)
![language](https://img.shields.io/badge/language-Python-green)
![license](https://img.shields.io/badge/license-MIT-orange)

ZeroFind, web sitelerinin ve ağ sistemlerinin güvenlik açıklarını tespit etmek için kullanılan kapsamlı bir tarama aracıdır. Hem terminal hem de web arayüzüne sahiptir. Türkçe dil desteği ile kullanıcı dostu bir deneyim sunar.

> **ÖNEMLİ**: Programı çalıştırmadan önce mutlaka `python setup.py` komutunu çalıştırarak gereksinimlerin tam olarak yüklendiğinden emin olun!

## 📋 Özellikler

- **Port Taraması**: Hedef sistemdeki açık portları tespit eder
- **Güvenlik Açığı Taraması**: Tespit edilen açık portlarda çalışan servislerdeki güvenlik açıklarını analiz eder
- **Özelleştirilebilir Tarama Seçenekleri**: Hızlı, standart veya derinlemesine tarama yapabilme
- **Kapsamlı Raporlama**: Tarama sonuçları detaylı grafikler ve açıklamalarla sunulur
- **Terminal ve Web Arayüzü**: İhtiyaca göre farklı kullanım seçenekleri
- **Platform Uyumluluğu**: Windows, Linux ve Android (Termux) sistemlerinde çalışabilme
- **Toplu Tarama**: Çoklu domainleri tek seferde tarayabilme
- **Dışa Aktarma**: Sonuçları JSON ve TXT formatında dışa aktarabilme

## 💻 Desteklenen Platformlar

- **Windows** (Windows 10, Windows 11)
- **Linux** (Ubuntu, Debian, CentOS, Fedora, Arch, vb.)
- **macOS**
- **Android** (Termux üzerinden)

## 🔧 Gereksinimler

- Python 3.8 veya üzeri
- Aşağıdaki Python kütüphaneleri:
  - Flask
  - Flask-SQLAlchemy
  - colorama
  - email-validator
  - gunicorn (Web sunucusu için)
  - psycopg2-binary (veritabanı bağlantısı için)

## 📥 Kurulum

### Windows

1. [Python](https://www.python.org/downloads/) yükleyin (3.8 veya üzeri)
2. Projeyi ZIP olarak indirin ve bir klasöre çıkarın
3. Komut istemini (cmd) açın ve klasöre gidin:
```cmd
cd yol\to\ZeroFind
```
4. Kurulum asistanını çalıştırın:
```cmd
python setup.py
```
5. Programı başlatın:
```cmd
python zerofind.py
```

### Linux

1. Python ve gerekli paketleri yükleyin:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```
2. Projeyi klonlayın:
```bash
git clone https://github.com/T5heAlyx/ZeroFind.git
cd ZeroFind
```
3. Sanal ortam oluşturun ve etkinleştirin (opsiyonel ama önerilen):
```bash
python3 -m venv venv
source venv/bin/activate
```
4. Kurulum asistanını çalıştırın:
```bash
python3 setup.py
```
5. Programı başlatın:
```bash
python3 zerofind.py
```

### macOS

1. [Homebrew](https://brew.sh/) kurulumunu yapın (yoksa)
2. Python yükleyin:
```bash
brew install python
```
3. Projeyi klonlayın:
```bash
git clone https://github.com/T5heAlyx/ZeroFind.git
cd ZeroFind
```
4. Kurulum asistanını çalıştırın:
```bash
python3 setup.py
```
5. Programı başlatın:
```bash
python3 zerofind.py
```

### Android (Termux)

1. [Termux](https://f-droid.org/en/packages/com.termux/) kurun (F-Droid üzerinden)
2. Termux'u açın ve gerekli paketleri yükleyin:
```bash
pkg update
pkg install python git
```
3. Projeyi klonlayın:
```bash
git clone https://github.com/T5heAlyx/ZeroFind.git
cd ZeroFind
```
4. Kurulum asistanını çalıştırın:
```bash
python setup.py
```
5. Programı başlatın:
```bash
python zerofind.py
```

## 🚀 Kullanım

### Terminal Arayüzü

Terminal arayüzünü başlatmak için:

```bash
python zerofind.py --terminal
```

Terminal arayüzünde aşağıdaki seçenekler mevcuttur:
1. Port Taraması Yap
2. Güvenlik Açığı Taraması Yap
3. Tam Güvenlik Analizi (Port + Zafiyet Taraması)
4. Toplu Domain Taraması
5. Tarama Sonuçlarını Kaydet (TXT)
6. Tarama Sonuçlarını Dışa Aktar (JSON)
7. Tarama Geçmişini Görüntüle
8. Yardım
9. Çıkış

### Web Arayüzü

Web arayüzünü başlatmak için:

```bash
python zerofind.py --web
```

Tarayıcınızdan `http://localhost:5000` adresine giderek web arayüzüne erişebilirsiniz.

### Komut Satırı Parametreleri

Program aşağıdaki parametrelerle çalıştırılabilir:

```
-t, --terminal    Terminal arayüzünü başlat
-w, --web         Web arayüzünü başlat
-p, --port        Web sunucusu port numarası (varsayılan: 5000)
-v, --verbose     Detaylı log çıktısı
--setup           Kurulum ve bağımlılık kontrolü yap
--version         Versiyon bilgisini göster
--url             Doğrudan tarama yapılacak URL
--scan-type       Tarama tipi (hızlı, standart, derinlemesine)
```

Örneğin:
```bash
python zerofind.py --url example.com --scan-type standart
```

### Tarama Tipleri

ZeroFind üç farklı tarama tipine sahiptir:

- **Hızlı Tarama**: Temel portları ve güvenlik açıklarını kontrol eder. Yaklaşık 1-2 dakika sürer.
- **Standart Tarama**: Daha fazla port ve güvenlik açığı kontrol eder. 5-15 dakika arası sürebilir.
- **Derinlemesine Tarama**: Tüm portları ve zafiyetleri kapsamlı şekilde kontrol eder. 20+ dakika sürebilir.

## 🔍 Tarama Özellikleri

### Port Taraması Özellikleri

- TCP portları taraması
- Servis tespiti
- Port durumu analizi (açık, filtrelenmiş)

### Güvenlik Açığı Taraması Özellikleri

- SSL/TLS zafiyetleri
- Web uygulama zafiyetleri (XSS, SQL Enjeksiyon, vb.)
- Sunucu yapılandırma hataları
- Protokol zafiyetleri
- Servis zafiyetleri

## 📊 Sonuçların Görüntülenmesi

### Terminal Arayüzü
Terminal arayüzünde, tarama sonuçları renkli tablolar halinde gösterilir. Önem derecelerine göre (düşük, orta, yüksek, kritik) zafiyetler renklendirilir.

### Web Arayüzü
Web arayüzünde, tarama sonuçları grafikler, tablolar ve açılır paneller şeklinde gösterilir. Sonuçları JSON veya TXT formatında dışa aktarabilirsiniz.

## ⚠️ Önemli Notlar

- Bu aracı yalnızca izin verilen sistemlerde kullanın.
- Yetkisiz kullanım yasal sonuçlar doğurabilir.
- Tarama sonuçları referans amaçlıdır, profesyonel güvenlik testlerinin yerini tutmaz.
- Bazı taramalar hedef sistemlere yük bindirebilir, gerçek üretim ortamlarında dikkatli kullanın.

## 🛠️ Sorun Giderme

### Bağımlılık Sorunları
Bağımlılık hatalarında:
```bash
pip install -r package_list.txt --force-reinstall
```

### Port Çakışmaları
Web arayüzü başlatırken port çakışması yaşarsanız, farklı bir port numarası belirtin:
```bash
python zerofind.py --web --port 8080
```

### Bağlantı Sorunları
Tarama sırasında bağlantı sorunları yaşıyorsanız, ağ ayarlarınızı ve güvenlik duvarınızı kontrol edin.

## 📫 İletişim ve Hata Bildirimi

Geri bildirimleriniz ve hata raporlarınız için GitHub'da issue açabilir veya aşağıdaki adresten iletişime geçebilirsiniz:
- Instagram: [@thewr4th](https://www.instagram.com/thewr4th/)
- Web sitesi: [wr4thinfo.github.io](https://wr4thinfo.github.io)

## 📜 Lisans

MIT Lisansı altında dağıtılmaktadır. Detaylar için `LICENSE` dosyasına bakınız.

## 👨‍💻 Credits

-made by wr4th0- (2025)
