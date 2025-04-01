#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZeroFind - Port Tarama Modülü
made by wr4th0 (https://wr4thinfo.github.io)
Versiyon: 2.0 (2025)
"""

import socket
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import re
from urllib.parse import urlparse

def extract_domain(target):
    """
    URL'den domain adını çıkarır
    Örnek: https://www.example.com/path -> www.example.com
    """
    # HTTP/HTTPS protokolü var mı kontrol et
    if target.startswith('http://') or target.startswith('https://'):
        parsed = urlparse(target)
        return parsed.netloc
    
    # URL path'i var mı kontrol et (example.com/path)
    if '/' in target and not target.startswith('/'):
        return target.split('/', 1)[0]
    
    return target

def is_valid_target(target):
    """
    Hedefin geçerli bir IP adresi veya domain adı olup olmadığını kontrol eder
    """
    # Önce URL'den domain adını çıkar
    domain = extract_domain(target)
    
    # Geçersiz karakterler varsa temizle
    domain = re.sub(r'[^a-zA-Z0-9.-]', '', domain)
    
    try:
        # Eğer domain ise, IP adresine çözümle
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def scan_ports(target, scan_type='hızlı'):
    """
    Hedefin açık portlarını tarar
    
    Args:
        target (str): Taranacak hedef (domain veya IP adresi)
        scan_type (str): Tarama tipi (hızlı, standart, derinlemesine)
        
    Returns:
        list: Açık portların listesi (dict formatında)
    """
    # Önce URL'den domain adını çıkar
    domain = extract_domain(target)
    
    # Geçersiz karakterler varsa temizle
    domain = re.sub(r'[^a-zA-Z0-9.-]', '', domain)
    
    # Hedefin geçerli olup olmadığını kontrol et
    if not is_valid_target(domain):
        raise ValueError(f"Geçersiz hedef: {target}")
    
    logging.info(f"Port taraması başlatılıyor: {target} ({scan_type})")
    
    # Tarama tipi ve parametrelerini belirle
    if scan_type == 'hızlı':
        # Yaygın 100 portu hızlıca tara
        port_range = [20, 21, 22, 23, 25, 53, 80, 110, 115, 119, 123, 143, 161, 
                      194, 443, 445, 465, 587, 993, 995, 1433, 1521, 3306, 3389, 
                      5432, 5900, 8080, 8443]
    elif scan_type == 'standart':
        # Daha fazla yaygın portu tara
        port_range = list(range(1, 1001))
    elif scan_type == 'derinlemesine':
        # Tüm portları tara (1-65535 arası)
        # Not: Bu çok fazla zaman alacağından sınırlayalım
        port_range = list(range(1, 10001))
    else:
        port_range = [20, 21, 22, 23, 25, 53, 80, 110, 115, 119, 123, 143, 161, 
                      194, 443, 445, 465, 587, 993, 995, 1433, 1521, 3306, 3389, 
                      5432, 5900, 8080, 8443]
    
    try:
        # Socket tabanlı tarama yap
        results = basic_port_scan(domain, port_range)
        return results
    
    except Exception as e:
        logging.error(f"Beklenmeyen hata: {str(e)}")
        raise

def quick_port_check(target, port):
    """
    Tek bir portu hızlıca kontrol etmek için yardımcı fonksiyon
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((target, port))
        if result == 0:  # Port açık
            return {'port': port, 'protocol': 'tcp', 'state': 'açık', 'service': 'bilinmiyor'}
        return None
    except:
        return None
    finally:
        sock.close()

def basic_port_scan(target, port_range=None):
    """
    nmap olmadan temel bir port taraması yapar (soket kullanarak)
    """
    if port_range is None:
        # Yaygın portlar
        port_range = [20, 21, 22, 23, 25, 53, 80, 110, 115, 119, 123, 143, 161, 
                      194, 443, 445, 465, 587, 993, 995, 1433, 1521, 3306, 3389, 
                      5432, 5900, 8080, 8443]
    
    results = []
    
    # Paralel olarak portları kontrol et
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(quick_port_check, target, port) for port in port_range]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
    
    return results
