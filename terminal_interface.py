#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZeroFind - Terminal Arayüzü
made by wr4th0 (https://wr4thinfo.github.io)
Versiyon: 2.0 (2025)
"""

import os
import sys
import time
import argparse
import logging
import platform
import json
from colorama import init, Fore, Back, Style
from port_scanner import scan_ports, is_valid_target, extract_domain
from vulnerability_scanner import check_vulnerabilities
from scanner import scan_target

init(autoreset=True, strip=False if platform.system() == 'Windows' else None)

# İşletim sistemi bilgisi
IS_WINDOWS = platform.system() == 'Windows'
IS_TERMUX = 'com.termux' in os.environ.get('PREFIX', '')

def print_banner():
    """Uygulama başlık bannerını gösterir"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║ {Fore.RED}███████╗███████╗██████╗  ██████╗ {Fore.BLUE}███████╗██╗███╗   ██╗██████╗  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.RED}╚══███╔╝██╔════╝██╔══██╗██╔═══██╗{Fore.BLUE}██╔════╝██║████╗  ██║██╔══██╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.RED}  ███╔╝ █████╗  ██████╔╝██║   ██║{Fore.BLUE}█████╗  ██║██╔██╗ ██║██║  ██║ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.RED} ███╔╝  ██╔══╝  ██╔══██╗██║   ██║{Fore.BLUE}██╔══╝  ██║██║╚██╗██║██║  ██║ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.RED}███████╗███████╗██║  ██║╚██████╔╝{Fore.BLUE}██║     ██║██║ ╚████║██████╔╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.RED}╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ {Fore.BLUE}╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝  {Fore.CYAN}║
{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════╣
{Fore.CYAN}║ {Fore.WHITE}                    Güvenlik Tarama Aracı                         {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}                     Versiyon: 2.0 (2025)                         {Fore.CYAN}║
{Fore.CYAN}║ {Fore.RED}                       made by wr4th0                            {Fore.CYAN}║
{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_menu():
    """Ana menüyü gösterir"""
    menu = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║ {Fore.WHITE}                         ANA MENÜ                               {Fore.CYAN}║
{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════╣
{Fore.CYAN}║ {Fore.GREEN}Tarama İşlemleri:{Fore.WHITE}                                                {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}1) {Fore.WHITE}Port Taraması Yap                                            {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}2) {Fore.WHITE}Güvenlik Açığı Taraması Yap                                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}3) {Fore.WHITE}Tam Güvenlik Analizi (Port + Zafiyet Taraması)              {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}4) {Fore.WHITE}Toplu Domain Taraması                                        {Fore.CYAN}║
{Fore.CYAN}║                                                                   {Fore.CYAN}║
{Fore.CYAN}║ {Fore.GREEN}Araçlar ve Raporlar:{Fore.WHITE}                                             {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}5) {Fore.WHITE}Tarama Sonuçlarını Kaydet (TXT)                             {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}6) {Fore.WHITE}Tarama Sonuçlarını Dışa Aktar (JSON)                        {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}7) {Fore.WHITE}Tarama Geçmişini Görüntüle                                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}8) {Fore.WHITE}Yardım                                                       {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}9) {Fore.WHITE}Çıkış                                                        {Fore.CYAN}║
{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝
"""
    print(menu)

def print_help():
    """Yardım bilgilerini gösterir"""
    help_text = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║ {Fore.WHITE}                   ZEROFIND YARDIM                             {Fore.CYAN}║
{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════╣
{Fore.CYAN}║ {Fore.WHITE}ZeroFind, web sitelerinin ve ağ sistemlerinin güvenlik            {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}açıklarını tespit etmek için kullanılan bir güvenlik tarama       {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}aracıdır.                                                         {Fore.CYAN}║
{Fore.CYAN}║                                                                   {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}Kullanım Örnekleri:{Fore.WHITE}                                              {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Tek bir web sitesi taramak için: örnek.com                      {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- IP adresi taramak için: 192.168.1.1                             {Fore.CYAN}║
{Fore.CYAN}║                                                                   {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}Tarama Tipleri:{Fore.WHITE}                                                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Hızlı Tarama: Temel portları ve güvenlik açıklarını kontrol     {Fore.CYAN}║
{Fore.CYAN}║   eder. Birkaç dakika sürer.                                      {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Standart Tarama: Daha fazla port ve açık kontrol eder. 5-15     {Fore.CYAN}║
{Fore.CYAN}║   dakika arası sürebilir.                                         {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Derinlemesine Tarama: Tüm portları ve zafiyetleri kontrol       {Fore.CYAN}║
{Fore.CYAN}║   eder. Uzun sürebilir, dikkatli kullanın.                        {Fore.CYAN}║
{Fore.CYAN}║                                                                   {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}Komut Satırı Kullanımı:{Fore.WHITE}                                          {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Tüm Arayüzler: python zerofind.py                               {Fore.CYAN}║
{Fore.CYAN}║   (Önce terminal, sonra web arayüzü)                              {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Sadece Terminal: python zerofind.py --terminal                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Sadece Web: python zerofind.py --web                            {Fore.CYAN}║
{Fore.CYAN}║                                                                   {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}Önemli Notlar:{Fore.WHITE}                                                   {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Bu aracı yalnızca izin verilen sistemlerde kullanın.            {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Yetkisiz kullanım yasal sonuçlar doğurabilir.                   {Fore.CYAN}║
{Fore.CYAN}║ {Fore.WHITE}- Web arayüzü için tarayıcınızda http://localhost:5000 adresini   {Fore.CYAN}║
{Fore.CYAN}║   ziyaret edin.                                                   {Fore.CYAN}║
{Fore.CYAN}║ {Fore.RED}- Made by wr4th0                                                   {Fore.CYAN}║
{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝
"""
    print(help_text)

def print_scan_options():
    """Tarama tipi seçeneklerini gösterir"""
    options = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║ {Fore.WHITE}                     TARAMA TİPİ SEÇİN                          {Fore.CYAN}║
{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════╣
{Fore.CYAN}║ {Fore.YELLOW}1) {Fore.WHITE}Hızlı Tarama      {Fore.BLUE}(Hızlı, temel kontroller)                {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}2) {Fore.WHITE}Standart Tarama   {Fore.BLUE}(Dengeli, çoğu açığı bulur)              {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}3) {Fore.WHITE}Derinlemesine     {Fore.BLUE}(Yavaş, kapsamlı kontroller)             {Fore.CYAN}║
{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝
"""
    print(options)

def display_progress(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """İlerleme çubuğu gösterir"""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{Fore.GREEN}{bar}{Style.RESET_ALL}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        print()

def display_port_results(results):
    """Port tarama sonuçlarını gösterir"""
    if not results:
        print(f"{Fore.YELLOW}[!] Açık port bulunamadı.")
        return
    
    print(f"\n{Fore.CYAN}╔════════╦════════╦══════════════╦═══════════════════╗")
    print(f"{Fore.CYAN}║ {Fore.WHITE}PORT   {Fore.CYAN}║ {Fore.WHITE}DURUM  {Fore.CYAN}║ {Fore.WHITE}PROTOKOL     {Fore.CYAN}║ {Fore.WHITE}SERVİS           {Fore.CYAN}║")
    print(f"{Fore.CYAN}╠════════╬════════╬══════════════╬═══════════════════╣")
    
    for port_info in results:
        port = str(port_info['port']).ljust(6)
        state = port_info['state'].ljust(6)
        protocol = port_info['protocol'].ljust(12)
        service = port_info['service'].ljust(17)
        
        state_color = Fore.GREEN if port_info['state'] == 'açık' else Fore.YELLOW
        
        print(f"{Fore.CYAN}║ {Fore.WHITE}{port} {Fore.CYAN}║ {state_color}{state} {Fore.CYAN}║ {Fore.WHITE}{protocol} {Fore.CYAN}║ {Fore.WHITE}{service} {Fore.CYAN}║")
    
    print(f"{Fore.CYAN}╚════════╩════════╩══════════════╩═══════════════════╝")

def display_vulnerability_results(results):
    """Zafiyet tarama sonuçlarını gösterir"""
    if not results:
        print(f"{Fore.GREEN}[✓] Herhangi bir güvenlik açığı tespit edilmedi.")
        return
    
    severity_colors = {
        'düşük': Fore.BLUE,
        'orta': Fore.YELLOW,
        'yüksek': Fore.RED,
        'kritik': Fore.RED + Style.BRIGHT
    }
    
    print(f"\n{Fore.CYAN}╔════════════════════════════════════════╦════════════╦════════════════════════════════╗")
    print(f"{Fore.CYAN}║ {Fore.WHITE}GÜVENLİK AÇIĞI                        {Fore.CYAN}║ {Fore.WHITE}SEVİYE      {Fore.CYAN}║ {Fore.WHITE}AÇIKLAMA                      {Fore.CYAN}║")
    print(f"{Fore.CYAN}╠════════════════════════════════════════╬════════════╬════════════════════════════════╣")
    
    for vuln in results:
        name = vuln['name'][:38].ljust(38)
        severity = vuln['severity'].ljust(10)
        desc = vuln['description'][:30] + '...'
        
        severity_color = severity_colors.get(vuln['severity'], Fore.WHITE)
        
        print(f"{Fore.CYAN}║ {Fore.WHITE}{name} {Fore.CYAN}║ {severity_color}{severity} {Fore.CYAN}║ {Fore.WHITE}{desc} {Fore.CYAN}║")
    
    print(f"{Fore.CYAN}╚════════════════════════════════════════╩════════════╩════════════════════════════════╝")
    
    # Detaylı açıklama ve öneriler
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║ {Fore.WHITE}                    DETAYLI AÇIKLAMALAR                         {Fore.CYAN}║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝")
    
    for i, vuln in enumerate(results, 1):
        severity_color = severity_colors.get(vuln['severity'], Fore.WHITE)
        print(f"\n{Fore.YELLOW}[{i}] {Fore.WHITE}{vuln['name']} {Fore.YELLOW}({severity_color}{vuln['severity']}{Fore.YELLOW})")
        print(f"{Fore.WHITE}Açıklama: {vuln['description']}")
        if 'recommendation' in vuln:
            print(f"{Fore.GREEN}Öneri: {vuln['recommendation']}")

def run_port_scan(target, scan_type):
    """Port taraması yapar ve sonuçları gösterir"""
    print(f"\n{Fore.YELLOW}[*] {target} için port taraması başlatılıyor ({scan_type})...")
    
    # İlerleme simülasyonu
    total_steps = 10
    for i in range(total_steps + 1):
        time.sleep(0.2)  # Tarama işlemi simülasyonu
        display_progress(i, total_steps, prefix=f'{Fore.BLUE}[*] Taranıyor:', 
                       suffix=f'{Fore.WHITE}Lütfen bekleyin...', length=40)
    
    # Asıl taramayı yap
    try:
        results = scan_ports(target, scan_type)
        print(f"\n{Fore.GREEN}[✓] Tarama tamamlandı! {len(results)} açık port bulundu.")
        display_port_results(results)
        return results
    except Exception as e:
        print(f"\n{Fore.RED}[!] Tarama sırasında hata oluştu: {str(e)}")
        return []

def run_vulnerability_scan(target, port_results, scan_type):
    """Zafiyet taraması yapar ve sonuçları gösterir"""
    print(f"\n{Fore.YELLOW}[*] {target} için zafiyet taraması başlatılıyor ({scan_type})...")
    
    # İlerleme simülasyonu
    total_steps = 15
    for i in range(total_steps + 1):
        time.sleep(0.3)  # Tarama işlemi simülasyonu
        display_progress(i, total_steps, prefix=f'{Fore.BLUE}[*] Zafiyetler kontrol ediliyor:', 
                       suffix=f'{Fore.WHITE}Lütfen bekleyin...', length=40)
    
    # Asıl taramayı yap
    try:
        results = check_vulnerabilities(target, port_results, scan_type)
        print(f"\n{Fore.GREEN}[✓] Zafiyet taraması tamamlandı! {len(results)} güvenlik açığı bulundu.")
        display_vulnerability_results(results)
        return results
    except Exception as e:
        print(f"\n{Fore.RED}[!] Zafiyet taraması sırasında hata oluştu: {str(e)}")
        return []

def run_full_security_scan(target, scan_type):
    """Tam güvenlik analizi yapar (port + zafiyet taraması)"""
    port_results = run_port_scan(target, scan_type)
    if port_results:
        vuln_results = run_vulnerability_scan(target, port_results, scan_type)
        
        # Özet rapor
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║ {Fore.WHITE}                       ÖZET RAPOR                              {Fore.CYAN}║")
        print(f"{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════╣")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Taranan Hedef: {Fore.YELLOW}{target.ljust(48)}{Fore.CYAN}║")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Tarama Tipi: {Fore.YELLOW}{scan_type.ljust(50)}{Fore.CYAN}║")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Tespit Edilen Açık Port Sayısı: {Fore.GREEN}{str(len(port_results)).ljust(34)}{Fore.CYAN}║")
        
        # Zafiyet sayılarını hesapla
        if vuln_results:
            low = sum(1 for v in vuln_results if v['severity'] == 'düşük')
            medium = sum(1 for v in vuln_results if v['severity'] == 'orta')
            high = sum(1 for v in vuln_results if v['severity'] == 'yüksek')
            critical = sum(1 for v in vuln_results if v['severity'] == 'kritik')
            
            print(f"{Fore.CYAN}║ {Fore.WHITE}Toplam Zafiyet Sayısı: {Fore.RED}{str(len(vuln_results)).ljust(41)}{Fore.CYAN}║")
            print(f"{Fore.CYAN}║ {Fore.WHITE} - Düşük Seviye: {Fore.BLUE}{str(low).ljust(49)}{Fore.CYAN}║")
            print(f"{Fore.CYAN}║ {Fore.WHITE} - Orta Seviye: {Fore.YELLOW}{str(medium).ljust(49)}{Fore.CYAN}║")
            print(f"{Fore.CYAN}║ {Fore.WHITE} - Yüksek Seviye: {Fore.RED}{str(high).ljust(47)}{Fore.CYAN}║")
            print(f"{Fore.CYAN}║ {Fore.WHITE} - Kritik Seviye: {Fore.RED + Style.BRIGHT}{str(critical).ljust(47)}{Fore.CYAN}║")
        else:
            print(f"{Fore.CYAN}║ {Fore.WHITE}Toplam Zafiyet Sayısı: {Fore.GREEN}0{' ' * 41}{Fore.CYAN}║")
        
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝")
        
        return port_results, vuln_results
    return [], []

def get_target_input():
    """Kullanıcıdan hedef girişi alır"""
    while True:
        target = input(f"{Fore.YELLOW}[?] Hedef adresi (domain veya IP): {Fore.WHITE}")
        
        if not target:
            print(f"{Fore.RED}[!] Hedef boş olamaz. Lütfen bir hedef girin.")
            continue
        
        if is_valid_target(target):
            return target
        else:
            print(f"{Fore.RED}[!] Geçersiz hedef. Lütfen geçerli bir domain adı veya IP adresi girin.")

def get_scan_type():
    """Kullanıcıdan tarama tipi seçimi alır"""
    print_scan_options()
    
    while True:
        choice = input(f"{Fore.YELLOW}[?] Seçiminiz (1-3): {Fore.WHITE}")
        
        if choice == '1':
            return 'hızlı'
        elif choice == '2':
            return 'standart'
        elif choice == '3':
            return 'derinlemesine'
        else:
            print(f"{Fore.RED}[!] Geçersiz seçim. Lütfen 1-3 arasında bir sayı girin.")

def save_scan_report(target, port_results, vuln_results, scan_type):
    """Tarama sonuçlarını dosyaya kaydeder"""
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"zerofind_scan_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            # Banner
            f.write("=" * 70 + "\n")
            f.write("                       ZEROFIND TARAMA RAPORU                      \n")
            f.write("=" * 70 + "\n\n")
            
            # Tarama bilgileri
            f.write("TARAMA BİLGİLERİ:\n")
            f.write("-" * 70 + "\n")
            f.write(f"Hedef: {target}\n")
            f.write(f"Tarama Tipi: {scan_type}\n")
            f.write(f"Tarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Toplam Açık Port: {len(port_results)}\n")
            f.write(f"Toplam Zafiyet: {len(vuln_results)}\n\n")
            
            # Port sonuçları
            f.write("AÇIK PORTLAR:\n")
            f.write("-" * 70 + "\n")
            if port_results:
                for port_info in port_results:
                    f.write(f"Port: {port_info['port']}, Durum: {port_info['state']}, ")
                    f.write(f"Protokol: {port_info['protocol']}, Servis: {port_info['service']}\n")
            else:
                f.write("Hiç açık port bulunamadı.\n")
            f.write("\n")
            
            # Zafiyet sonuçları
            f.write("GÜVENLİK AÇIKLARI:\n")
            f.write("-" * 70 + "\n")
            if vuln_results:
                for i, vuln in enumerate(vuln_results, 1):
                    f.write(f"[{i}] {vuln['name']} (Seviye: {vuln['severity']})\n")
                    f.write(f"    Açıklama: {vuln['description']}\n")
                    if 'recommendation' in vuln:
                        f.write(f"    Öneri: {vuln['recommendation']}\n")
                    f.write("\n")
            else:
                f.write("Hiç güvenlik açığı bulunamadı.\n")
            
            # Footer
            f.write("\n" + "=" * 70 + "\n")
            f.write("                ZeroFind - made by wr4th0                \n")
            f.write("=" * 70 + "\n")
        
        print(f"\n{Fore.GREEN}[✓] Tarama raporu '{filename}' dosyasına kaydedildi.")
        return filename
    except Exception as e:
        print(f"\n{Fore.RED}[!] Rapor kaydetme hatası: {str(e)}")
        return None


def export_scan_to_json(target, port_results, vuln_results, scan_type):
    """Tarama sonuçlarını JSON formatında kaydeder"""
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"zerofind_scan_{timestamp}.json"
        
        data = {
            "scan_info": {
                "target": target,
                "scan_type": scan_type,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_open_ports": len(port_results),
                "total_vulnerabilities": len(vuln_results)
            },
            "open_ports": port_results,
            "vulnerabilities": vuln_results
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"\n{Fore.GREEN}[✓] Tarama raporu JSON formatında '{filename}' dosyasına kaydedildi.")
        return filename
    except Exception as e:
        print(f"\n{Fore.RED}[!] JSON raporu kaydetme hatası: {str(e)}")
        return None


def run_batch_scan():
    """Toplu domain taraması yapar"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║ {Fore.WHITE}                     TOPLU DOMAIN TARAMASI                     {Fore.CYAN}║")
    print(f"{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}║ {Fore.WHITE}1. Domain listesini bir metin dosyasından okuyabilirsiniz.     {Fore.CYAN}║")
    print(f"{Fore.CYAN}║ {Fore.WHITE}2. Her satırda bir domain olmalıdır.                           {Fore.CYAN}║")
    print(f"{Fore.CYAN}║ {Fore.WHITE}3. Tüm domainler aynı tarama tipiyle taranacaktır.             {Fore.CYAN}║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝")
    
    # Dosya seçimi
    while True:
        filename = input(f"\n{Fore.YELLOW}[?] Domain listesi dosyasının adı (örn: domains.txt): {Fore.WHITE}")
        
        if not filename:
            print(f"{Fore.RED}[!] Dosya adı boş olamaz.")
            continue
            
        try:
            with open(filename, 'r') as f:
                domains = [line.strip() for line in f if line.strip()]
                
            if not domains:
                print(f"{Fore.RED}[!] Dosya boş veya okunamadı.")
                continue
                
            print(f"{Fore.GREEN}[✓] {len(domains)} domain okundu.")
            break
        except FileNotFoundError:
            print(f"{Fore.RED}[!] Dosya bulunamadı: {filename}")
        except Exception as e:
            print(f"{Fore.RED}[!] Dosya okuma hatası: {str(e)}")
    
    # Tarama tipi seçimi
    scan_type = get_scan_type()
    
    # Tarama sonuçları
    batch_results = []
    
    print(f"\n{Fore.YELLOW}[*] Toplu tarama başlatılıyor...")
    print(f"{Fore.YELLOW}[*] Toplam domain sayısı: {len(domains)}")
    
    # Her bir domain için tarama yap
    for i, domain in enumerate(domains, 1):
        print(f"\n{Fore.CYAN}[{i}/{len(domains)}] {domain} taranıyor...")
        
        try:
            # Domain geçerli mi kontrol et
            if not is_valid_target(domain):
                print(f"{Fore.RED}[!] Geçersiz domain: {domain}, atlanıyor.")
                continue
                
            # Tarama yap
            port_results = run_port_scan(domain, scan_type)
            
            if port_results:
                vuln_results = run_vulnerability_scan(domain, port_results, scan_type)
                
                # Sonuçları ekle
                batch_results.append({
                    'domain': domain,
                    'ports': port_results,
                    'vulnerabilities': vuln_results
                })
        except Exception as e:
            print(f"{Fore.RED}[!] {domain} taraması sırasında hata: {str(e)}")
    
    # Toplu tarama özeti
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║ {Fore.WHITE}                     TOPLU TARAMA SONUÇLARI                    {Fore.CYAN}║")
    print(f"{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Taranan Domain Sayısı: {Fore.YELLOW}{str(len(domains)).ljust(40)}{Fore.CYAN}║")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Başarılı Tarama Sayısı: {Fore.GREEN}{str(len(batch_results)).ljust(39)}{Fore.CYAN}║")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Tarama Tipi: {Fore.YELLOW}{scan_type.ljust(50)}{Fore.CYAN}║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝")
    
    # Toplu sonuçları kaydet
    if batch_results:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"zerofind_batch_scan_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(batch_results, f, ensure_ascii=False, indent=4)
                
            print(f"\n{Fore.GREEN}[✓] Toplu tarama sonuçları '{filename}' dosyasına kaydedildi.")
        except Exception as e:
            print(f"\n{Fore.RED}[!] Toplu tarama sonuçları kaydedilemedi: {str(e)}")
    
    return batch_results


def display_scan_history(scan_history):
    """Tarama geçmişini gösterir"""
    if not scan_history:
        print(f"\n{Fore.YELLOW}[!] Henüz tarama geçmişi bulunmuyor.")
        return
    
    print(f"\n{Fore.CYAN}╔════════╦══════════════════════════════╦════════════╦════════════╦════════════╗")
    print(f"{Fore.CYAN}║ {Fore.WHITE}ID     {Fore.CYAN}║ {Fore.WHITE}HEDEF                        {Fore.CYAN}║ {Fore.WHITE}TİP        {Fore.CYAN}║ {Fore.WHITE}PORTLAR    {Fore.CYAN}║ {Fore.WHITE}ZAFİYETLER {Fore.CYAN}║")
    print(f"{Fore.CYAN}╠════════╬══════════════════════════════╬════════════╬════════════╬════════════╣")
    
    for i, scan in enumerate(scan_history, 1):
        id_str = str(i).ljust(6)
        target = scan['target'][:26].ljust(26)
        scan_type = scan['scan_type'].ljust(10)
        ports_count = str(len(scan['ports'])).ljust(10)
        vulns_count = str(len(scan['vulnerabilities'])).ljust(10)
        
        print(f"{Fore.CYAN}║ {Fore.WHITE}{id_str} {Fore.CYAN}║ {Fore.WHITE}{target} {Fore.CYAN}║ {Fore.WHITE}{scan_type} {Fore.CYAN}║ {Fore.WHITE}{ports_count} {Fore.CYAN}║ {Fore.WHITE}{vulns_count} {Fore.CYAN}║")
    
    print(f"{Fore.CYAN}╚════════╩══════════════════════════════╩════════════╩════════════╩════════════╝")
    
    # Geçmiş kayıtları hakkında detaylı bilgi
    while True:
        choice = input(f"\n{Fore.YELLOW}[?] Detaylı görüntülemek istediğiniz tarama ID'si (İptal için 0): {Fore.WHITE}")
        
        if choice == '0':
            return
            
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(scan_history):
                scan = scan_history[idx]
                
                print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
                print(f"{Fore.CYAN}║ {Fore.WHITE}                     TARAMA DETAYLARI                          {Fore.CYAN}║")
                print(f"{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════╣")
                print(f"{Fore.CYAN}║ {Fore.WHITE}Hedef: {Fore.YELLOW}{scan['target'].ljust(53)}{Fore.CYAN}║")
                print(f"{Fore.CYAN}║ {Fore.WHITE}Tarama Tipi: {Fore.YELLOW}{scan['scan_type'].ljust(49)}{Fore.CYAN}║")
                print(f"{Fore.CYAN}║ {Fore.WHITE}Tarih: {Fore.YELLOW}{scan['date'].ljust(54)}{Fore.CYAN}║")
                print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝")
                
                # Port sonuçlarını göster
                display_port_results(scan['ports'])
                
                # Zafiyet sonuçlarını göster
                display_vulnerability_results(scan['vulnerabilities'])
                
                break
            else:
                print(f"{Fore.RED}[!] Geçersiz ID. Lütfen 1-{len(scan_history)} arasında bir sayı girin.")
        except ValueError:
            print(f"{Fore.RED}[!] Geçersiz değer. Lütfen bir sayı girin.")


def run_terminal_interface():
    """Terminal arayüzü ana döngüsü"""
    # İşlem geçmişini tut
    scan_history = []
    
    # Son yapılan tarama sonuçları
    last_scan = {
        'target': '',
        'scan_type': '',
        'ports': [],
        'vulnerabilities': []
    }
    
    # Termux, Linux ve Windows'da çalışacak şekilde ekran temizleme
    try:
        if IS_WINDOWS:
            os.system('cls')
        elif IS_TERMUX:
            os.system('clear')
        else:
            os.system('clear')
    except:
        # Ekran temizleme başarısız olursa birkaç satır boşluk bırak
        print("\n" * 100)
    print_banner()
    
    while True:
        print_menu()
        choice = input(f"{Fore.YELLOW}[?] Seçiminiz (1-9): {Fore.WHITE}")
        
        if choice == '1':  # Port Taraması
            target = get_target_input()
            scan_type = get_scan_type()
            port_results = run_port_scan(target, scan_type)
            
            # Geçmiş kaydını güncelle
            last_scan = {
                'target': target,
                'scan_type': scan_type,
                'date': time.strftime("%Y-%m-%d %H:%M:%S"),
                'ports': port_results,
                'vulnerabilities': []
            }
            scan_history.append(last_scan.copy())
            
        elif choice == '2':  # Zafiyet Taraması
            target = get_target_input()
            scan_type = get_scan_type()
            port_results = run_port_scan(target, scan_type)
            
            vuln_results = []
            if port_results:
                vuln_results = run_vulnerability_scan(target, port_results, scan_type)
            
            # Geçmiş kaydını güncelle
            last_scan = {
                'target': target,
                'scan_type': scan_type,
                'date': time.strftime("%Y-%m-%d %H:%M:%S"),
                'ports': port_results,
                'vulnerabilities': vuln_results
            }
            scan_history.append(last_scan.copy())
                
        elif choice == '3':  # Tam Güvenlik Analizi
            target = get_target_input()
            scan_type = get_scan_type()
            port_results, vuln_results = run_full_security_scan(target, scan_type)
            
            # Geçmiş kaydını güncelle
            last_scan = {
                'target': target,
                'scan_type': scan_type,
                'date': time.strftime("%Y-%m-%d %H:%M:%S"),
                'ports': port_results,
                'vulnerabilities': vuln_results
            }
            scan_history.append(last_scan.copy())
            
        elif choice == '4':  # Toplu Domain Taraması
            batch_results = run_batch_scan()
            
        elif choice == '5':  # Tarama Sonuçlarını Kaydet (TXT)
            if not last_scan['target']:
                print(f"\n{Fore.RED}[!] Önce bir tarama yapmalısınız.")
            else:
                save_scan_report(
                    last_scan['target'], 
                    last_scan['ports'], 
                    last_scan['vulnerabilities'], 
                    last_scan['scan_type']
                )
                
        elif choice == '6':  # Tarama Sonuçlarını Dışa Aktar (JSON)
            if not last_scan['target']:
                print(f"\n{Fore.RED}[!] Önce bir tarama yapmalısınız.")
            else:
                export_scan_to_json(
                    last_scan['target'], 
                    last_scan['ports'], 
                    last_scan['vulnerabilities'], 
                    last_scan['scan_type']
                )
                
        elif choice == '7':  # Tarama Geçmişini Görüntüle
            display_scan_history(scan_history)
            
        elif choice == '8':  # Yardım
            print_help()
            
        elif choice == '9':  # Çıkış
            print(f"\n{Fore.GREEN}[✓] ZeroFind'dan çıkılıyor. İyi günler!")
            break
            
        else:
            print(f"{Fore.RED}[!] Geçersiz seçim. Lütfen 1-9 arasında bir sayı girin.")
        
        input(f"\n{Fore.CYAN}[*] Devam etmek için Enter tuşuna basın...")
        # Termux, Linux ve Windows'da çalışacak şekilde ekran temizleme
        try:
            if IS_WINDOWS:
                os.system('cls')
            elif IS_TERMUX:
                os.system('clear')
            else:
                os.system('clear')
        except:
            # Ekran temizleme başarısız olursa birkaç satır boşluk bırak
            print("\n" * 100)
        print_banner()

if __name__ == "__main__":
    run_terminal_interface()
run_terminal_interface()
