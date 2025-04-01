#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZeroFind - Veritabanı Modelleri
made by wr4th0 (https://wr4thinfo.github.io)
Versiyon: 2.0 (2025)
"""

from app import db
from datetime import datetime

class ScanResult(db.Model):
    """Tarama sonuçlarının ana tablosu"""
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(255), nullable=False)
    scan_date = db.Column(db.DateTime, default=datetime.utcnow)
    scan_type = db.Column(db.String(50), default='hızlı')  # hızlı, standart, derinlemesine
    status = db.Column(db.String(50), default='tamamlandı')  # başladı, tamamlandı, başarısız
    duration = db.Column(db.Float, default=0.0)  # saniye cinsinden tarama süresi
    
    # İlişkiler
    open_ports = db.relationship('OpenPort', backref='scan', lazy=True, cascade="all, delete-orphan")
    vulnerabilities = db.relationship('VulnerabilityFound', backref='scan', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Tarama #{self.id} - {self.target}>'

class OpenPort(db.Model):
    """Açık port bilgilerini saklayan tablo"""
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan_result.id'), nullable=False)
    port_number = db.Column(db.Integer, nullable=False)
    protocol = db.Column(db.String(10), default='tcp')  # tcp, udp
    service_name = db.Column(db.String(100))
    state = db.Column(db.String(20), default='açık')  # açık, filtrelenmiş
    version_info = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Port {self.port_number}/{self.protocol}>'

class VulnerabilityFound(db.Model):
    """Tespit edilen güvenlik açıklarını saklayan tablo"""
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan_result.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(20), default='orta')  # düşük, orta, yüksek, kritik
    description = db.Column(db.Text)
    cve_id = db.Column(db.String(20))  # CVE numarası, varsa
    recommendation = db.Column(db.Text)  # Önerilen çözüm
    
    def __repr__(self):
        return f'<Zafiyet {self.name} ({self.severity})>'
