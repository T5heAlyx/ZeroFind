#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZeroFind - Tarama Motorunu Çalıştıran Ana Modül
made by wr4th0 (https://wr4thinfo.github.io)
Versiyon: 2.0 (2025)
"""

import time
import logging
from app import db
from models import ScanResult, OpenPort, VulnerabilityFound
from port_scanner import scan_ports
from vulnerability_scanner import check_vulnerabilities

def scan_target(target, scan_type='hızlı'):
    """
    Hedef siteyi tarar ve sonuçları veritabanına kaydeder
    
    Args:
        target (str): Taranacak hedef (domain veya IP adresi)
        scan_type (str): Tarama tipi (hızlı, standart, derinlemesine)
        
    Returns:
        int: Oluşturulan tarama kaydının ID'si
    """
    logging.info(f"'{target}' için {scan_type} tarama başlatılıyor...")
    
    # Yeni tarama kaydı oluştur
    scan_result = ScanResult(
        target=target,
        scan_type=scan_type,
        status='başladı'
    )
    db.session.add(scan_result)
    db.session.commit()
    
    start_time = time.time()
    
    try:
        # Port taraması yap
        logging.info(f"Port taraması başlatılıyor: {target}")
        port_results = scan_ports(target, scan_type)
        
        # Açık portları kaydet
        for port_info in port_results:
            open_port = OpenPort(
                scan_id=scan_result.id,
                port_number=port_info['port'],
                protocol=port_info['protocol'],
                service_name=port_info['service'],
                state=port_info['state'],
                version_info=port_info.get('version', '')
            )
            db.session.add(open_port)
        
        # Zafiyet taraması yap
        logging.info(f"Zafiyet taraması başlatılıyor: {target}")
        vulnerability_results = check_vulnerabilities(target, port_results, scan_type)
        
        # Tespit edilen zafiyetleri kaydet
        for vuln_info in vulnerability_results:
            vulnerability = VulnerabilityFound(
                scan_id=scan_result.id,
                name=vuln_info['name'],
                severity=vuln_info['severity'],
                description=vuln_info['description'],
                cve_id=vuln_info.get('cve_id', ''),
                recommendation=vuln_info.get('recommendation', '')
            )
            db.session.add(vulnerability)
        
        # Tarama tamamlandı olarak işaretle
        scan_result.status = 'tamamlandı'
        scan_result.duration = time.time() - start_time
        db.session.commit()
        
        logging.info(f"Tarama tamamlandı: {target}")
        return scan_result.id
        
    except Exception as e:
        # Hata durumunda
        logging.error(f"Tarama sırasında hata: {str(e)}")
        scan_result.status = 'başarısız'
        scan_result.duration = time.time() - start_time
        db.session.commit()
        raise e
