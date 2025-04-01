#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZeroFind - Kapsamlı Güvenlik Tarama Aracı
Geliştiren: wr4th0 (https://wr4thinfo.github.io)
"""

import sys
import argparse
import logging
import os
from datetime import datetime

# Terminal renkli çıktılar için
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # Colorama yüklü değilse, renkli çıktı olmayan sürümü kullan
    class Dummy:
        def __getattr__(self, name):
            return ""
    
    class DummyStyle:
        BRIGHT = ""
        RESET_ALL = ""
    
    Fore = Dummy()
    Style = DummyStyle()

# Ana modüller
from app import app
from terminal_interface import run_terminal_interface, print_banner
from setup import main as setup_main

def parse_arguments():
    """Komut satırı argümanlarını ayrıştırır"""
    parser = argparse.ArgumentParser(description='ZeroFind - Güvenlik Tarama Aracı')
    parser.add_argument('-t', '--terminal', action='store_true', help='Terminal arayüzünü başlat')
    parser.add_argument('-w', '--web', action='store_true', help='Web arayüzünü başlat')
    parser.add_argument('-p', '--port', type=int, default=5000, help='Web sunucusu port numarası')
    parser.add_argument('-v', '--verbose', action='store_true', help='Detaylı log çıktısı')
    parser.add_argument('--setup', action='store_true', help='Kurulum ve bağımlılık kontrolü yap')
    parser.add_argument('--version', action='store_true', help='Versiyon bilgisini göster')
    parser.add_argument('--url', type=str, help='Doğrudan tarama yapılacak URL')
    parser.add_argument('--scan-type', type=str, choices=['hızlı', 'standart', 'derinlemesine'], 
                        default='hızlı', help='Tarama tipi (hızlı, standart, derinlemesine)')
    
    return parser.parse_args()

def show_version():
    """Versiyon bilgisini gösterir"""
    version = "1.0.0"
    build_date = "01.04.2025"
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}ZeroFind v{version}")
    print(f"{Fore.WHITE}Geliştiren: {Fore.GREEN}wr4th0 {Fore.WHITE}(https://wr4thinfo.github.io)")
    print(f"{Fore.WHITE}Build: {build_date}")
    print(f"{Fore.WHITE}Lisans: MIT\n")

def configure_logging(level=logging.INFO):
    """Log yapılandırmasını ayarlar"""
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=level, format=log_format, datefmt=date_format)

def scan_from_cli(url, scan_type):
    """Doğrudan komut satırından tarama yapar"""
    from scanner import scan_target
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}ZeroFind - CLI Tarama")
    print(f"{Fore.WHITE}Hedef: {Fore.GREEN}{url}")
    print(f"{Fore.WHITE}Tarama Tipi: {Fore.GREEN}{scan_type}")
    print(f"{Fore.WHITE}Tarih: {Fore.GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.YELLOW}Tarama başlatılıyor, lütfen bekleyin...\n")
    
    try:
        # Taramayı başlat
        scan_id = scan_target(url, scan_type)
        
        if scan_id:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}Tarama Tamamlandı!")
            print(f"{Fore.WHITE}Tarama ID: {Fore.GREEN}{scan_id}")
            print(f"{Fore.WHITE}Sonucu web arayüzünden görüntüleyin: {Fore.CYAN}http://localhost:5000/results/{scan_id}")
            
            # Web arayüzünü başlat
            print(f"\n{Fore.YELLOW}Web arayüzü başlatılıyor (CTRL+C ile çıkabilirsiniz)...")
            app.run(host="0.0.0.0", port=5000, debug=False)
        else:
            print(f"{Fore.RED}Tarama başarısız oldu!")
    except Exception as e:
        print(f"{Fore.RED}Hata: {str(e)}")

def main():
    """Ana fonksiyon"""
    args = parse_arguments()
    
    # Bağımlılık kontrolü
    if args.setup:
        setup_main()
        return
        
    # Detaylı log çıktısı
    log_level = logging.DEBUG if args.verbose else logging.INFO
    configure_logging(log_level)
    
    # Versiyon bilgisi
    if args.version:
        show_version()
        return
    
    # Doğrudan URL taraması
    if args.url:
        scan_from_cli(args.url, args.scan_type)
        return
    
    # Varsayılan olarak web arayüzünü başlat
    if not (args.terminal or args.web):
        print_banner()
        print(f"{Fore.YELLOW}Kullanım için -h veya --help parametresi kullanabilirsiniz.")
        print(f"{Fore.CYAN}Varsayılan olarak web arayüzü başlatılıyor...\n")
        app.run(host="0.0.0.0", port=args.port, debug=True)
        return
    
    # Terminal arayüzü
    if args.terminal:
        print_banner()
        run_terminal_interface()
        return
    
    # Web arayüzü
    if args.web:
        print_banner()
        print(f"{Fore.CYAN}Web arayüzü başlatılıyor: http://localhost:{args.port}")
        app.run(host="0.0.0.0", port=args.port, debug=True)
        return

if __name__ == "__main__":
    main()