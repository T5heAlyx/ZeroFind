#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZeroFind - Kurulum ve Bağımlılık Kontrolü
made by wr4th0 (https://wr4thinfo.github.io)
Versiyon: 2.0 (2025)
"""

import subprocess
import sys
import os
import importlib.util
import platform

def check_python_version():
    """Python versiyonunu kontrol et"""
    print("\n[*] Python versiyonu kontrol ediliyor...")
    required_version = (3, 8)
    current_version = sys.version_info
    
    if current_version >= required_version:
        print(f"[✓] Python {current_version.major}.{current_version.minor}.{current_version.micro} sürümü uygun.")
        return True
    else:
        print(f"[!] Python {required_version[0]}.{required_version[1]} veya daha yeni bir sürüm gerekli.")
        print(f"[!] Mevcut sürüm: Python {current_version.major}.{current_version.minor}.{current_version.micro}")
        return False

def is_package_installed(package_name):
    """Bir paketin yüklü olup olmadığını kontrol et"""
    spec = importlib.util.find_spec(package_name.split('==')[0])
    return spec is not None

def read_requirements():
    """package_list.txt dosyasından gereksinimleri oku"""
    try:
        with open('package_list.txt', 'r') as file:
            requirements = [line.strip() for line in file if line.strip()]
        return requirements
    except FileNotFoundError:
        print("[!] package_list.txt dosyası bulunamadı.")
        return None

def install_requirements(requirements):
    """Gereksinimleri yükle"""
    pip_command = [sys.executable, "-m", "pip", "install"]
    installed_count = 0
    already_installed_count = 0
    failed_count = 0
    
    for req in requirements:
        package_name = req.split('==')[0]
        
        if is_package_installed(package_name):
            print(f"[✓] {req} zaten yüklü.")
            already_installed_count += 1
            continue
        
        print(f"[*] {req} yükleniyor...")
        try:
            subprocess.check_call(pip_command + [req], stdout=subprocess.DEVNULL)
            print(f"[✓] {req} başarıyla yüklendi.")
            installed_count += 1
        except subprocess.CalledProcessError:
            print(f"[!] {req} yüklenirken hata oluştu.")
            failed_count += 1
    
    return installed_count, already_installed_count, failed_count

def check_colorama():
    """Colorama yüklü değilse yükle (terminal renkli çıktıları için)"""
    if not is_package_installed("colorama"):
        print("[*] Terminal renklendirmesi için Colorama paketi yükleniyor...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"], 
                                 stdout=subprocess.DEVNULL)
            print("[✓] Colorama başarıyla yüklendi.")
            # Yeni yüklendiği için modülü yeniden yükleyelim
            globals()["colorama"] = importlib.import_module("colorama")
            globals()["colorama"].init()
        except subprocess.CalledProcessError:
            print("[!] Colorama yüklenirken hata oluştu, renkli çıktılar devre dışı olacak.")
    else:
        # Colorama zaten yüklü, import edelim
        globals()["colorama"] = importlib.import_module("colorama")
        globals()["colorama"].init()

def check_system_compatibility():
    """Sistem uyumluluğunu kontrol et"""
    system = platform.system()
    print(f"[*] İşletim sistemi: {system}")
    
    if system == "Windows":
        print("[i] Windows sisteminde çalışıyor. Tam uyumluluk için Windows Terminal kullanmanız önerilir.")
    elif system == "Linux":
        print("[i] Linux sisteminde çalışıyor. ZeroFind Linux sistemlerinde tam uyumludur.")
    elif system == "Darwin":
        print("[i] MacOS sisteminde çalışıyor. ZeroFind MacOS sistemlerinde genellikle uyumludur.")
    else:
        print(f"[!] Bilinmeyen işletim sistemi: {system}. Beklenmeyen davranışlar olabilir.")
    
    # Termux kontrolü
    if os.environ.get('PREFIX', '').find('com.termux') != -1:
        print("[i] Termux ortamında çalışıyor. ZeroFind Termux'ta uyumlu olacak şekilde ayarlanmıştır.")

def main():
    """Ana fonksiyon"""
    # Banner göster
    print("\n" + "=" * 70)
    print("                      ZeroFind Kurulum Asistanı")
    print("=" * 70)
    
    # Colorama kontrolü
    check_colorama()
    try:
        from colorama import Fore, Style
        print(f"{Fore.CYAN}[i] Renkli terminal çıktısı aktif.{Style.RESET_ALL}")
    except ImportError:
        pass
    
    # Python versiyonu kontrolü
    if not check_python_version():
        print("\n[!] Uyumsuz Python sürümü. Kurulum iptal ediliyor.")
        return False
    
    # Sistem uyumluluğu kontrolü
    check_system_compatibility()
    
    # Gereksinimleri oku
    print("\n[*] Gerekli paketler kontrol ediliyor...")
    requirements = read_requirements()
    if not requirements:
        print("[!] Gereksinimler okunamadı. Kurulum iptal ediliyor.")
        return False
    
    # Gereksinimleri yükle
    installed, already_installed, failed = install_requirements(requirements)
    
    # Sonuçları göster
    print("\n" + "=" * 70)
    print(f"[*] Toplam paket: {len(requirements)}")
    try:
        from colorama import Fore, Style
        print(f"{Fore.GREEN}[✓] Zaten yüklü: {already_installed}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Yeni yüklenen: {installed}{Style.RESET_ALL}")
        if failed > 0:
            print(f"{Fore.RED}[!] Başarısız: {failed}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[✓] Başarısız: {failed}{Style.RESET_ALL}")
    except ImportError:
        print(f"[✓] Zaten yüklü: {already_installed}")
        print(f"[✓] Yeni yüklenen: {installed}")
        print(f"[!] Başarısız: {failed}")
    
    # Kurulum sonucunu değerlendir
    if failed == 0:
        print("\n[✓] Tüm bağımlılıklar kuruldu! ZeroFind'ı şimdi kullanabilirsiniz.")
        print("[*] Başlatmak için: python zerofind.py")
        return True
    else:
        print("\n[!] Bazı paketler yüklenemedi. Lütfen hataları kontrol edin ve yeniden deneyin.")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        choice = input("\nZeroFind'ı şimdi başlatmak ister misiniz? (e/h): ")
        if choice.lower() in ['e', 'evet', 'y', 'yes']:
            print("\n[*] ZeroFind başlatılıyor...")
            try:
                subprocess.call([sys.executable, "zerofind.py"])
            except Exception as e:
                print(f"[!] Başlatma sırasında hata oluştu: {str(e)}")
        else:
            print("\n[*] ZeroFind'ı daha sonra başlatmak için 'python zerofind.py' komutunu kullanabilirsiniz.")
    
    print("\n[*] Kurulum asistanı tamamlandı.")