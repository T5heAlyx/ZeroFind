#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZeroFind - Flask Web Uygulaması
made by wr4th0 (https://wr4thinfo.github.io)
Versiyon: 2.0 (2025)
"""

import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
# made by wr4th0
app.secret_key = "zerofind_gizli_anahtar_2025"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///zerofind.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)

from scanner import scan_target
from models import ScanResult, VulnerabilityFound, OpenPort

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    # Toplu tarama modu mu kontrolü
    enable_batch = request.form.get('enable_batch') == 'on'
    scan_type = request.form.get('scan_type', 'hızlı')
    
    # Toplu tarama modu
    if enable_batch:
        # Dosya yükleme kontrolü
        if 'domain_file' not in request.files:
            flash('Lütfen bir domain listesi dosyası yükleyin.', 'danger')
            return redirect(url_for('index'))
            
        file = request.files['domain_file']
        
        if file.filename == '':
            flash('Dosya seçilmedi.', 'danger')
            return redirect(url_for('index'))
            
        if file:
            # Dosyadan domainleri oku
            try:
                content = file.read().decode('utf-8')
                domains = [line.strip() for line in content.split('\n') if line.strip()]
                
                if not domains:
                    flash('Domain listesi boş.', 'danger')
                    return redirect(url_for('index'))
                
                # Tüm domainleri tara ve sonuçları sakla
                scan_ids = []
                for domain in domains:
                    try:
                        scan_id = scan_target(domain, scan_type)
                        scan_ids.append(scan_id)
                    except Exception as e:
                        logging.error(f"Toplu tarama hatası ({domain}): {str(e)}")
                        # Hata olsa bile diğer domainleri taramaya devam et
                
                # Sonuçları göster
                flash(f'{len(scan_ids)} domain başarıyla tarandı.', 'success')
                
                # İlk taramanın sonuçlarını göster veya tarama geçmişine yönlendir
                if scan_ids:
                    return redirect(url_for('results', scan_id=scan_ids[0]))
                else:
                    return redirect(url_for('history'))
                    
            except Exception as e:
                logging.error(f"Toplu tarama dosya okuma hatası: {str(e)}")
                flash(f'Toplu tarama sırasında bir hata oluştu: {str(e)}', 'danger')
                return redirect(url_for('index'))
    
    # Tekli tarama modu
    else:
        target = request.form.get('target')
        
        if not target:
            flash('Lütfen bir hedef belirtin.', 'danger')
            return redirect(url_for('index'))
        
        try:
            # Yeni tarama işlemi başlat
            scan_id = scan_target(target, scan_type)
            
            # Tarama sonuçları sayfasına yönlendir
            return redirect(url_for('results', scan_id=scan_id))
        except Exception as e:
            logging.error(f"Tarama hatası: {str(e)}")
            flash(f'Tarama sırasında bir hata oluştu: {str(e)}', 'danger')
            return redirect(url_for('index'))

# Tarama sonuçları sayfası
@app.route('/results/<int:scan_id>')
def results(scan_id):
    # Tarama sonucunu veritabanından al
    scan_result = ScanResult.query.get_or_404(scan_id)
    
    # İlgili açık portları ve zafiyetleri de al
    open_ports = OpenPort.query.filter_by(scan_id=scan_id).all()
    vulnerabilities = VulnerabilityFound.query.filter_by(scan_id=scan_id).all()
    
    return render_template('results.html', 
                          scan=scan_result, 
                          open_ports=open_ports, 
                          vulnerabilities=vulnerabilities)

# Tüm tarama geçmişini gör
@app.route('/history')
def history():
    # Tüm taramaları zamanlarına göre sırala (en yeniden en eskiye)
    all_scans = ScanResult.query.order_by(ScanResult.scan_date.desc()).all()
    return render_template('results.html', history=all_scans)

# Hakkında sayfası
@app.route('/about')
def about():
    return render_template('about.html')

# Terminal arayüzü
@app.route('/terminal')
def terminal():
    import subprocess
    import sys
    
    # Terminal arayüzünü çalıştır
    return render_template('terminal.html')

# API: Tarama sonuçlarını JSON olarak döndür
@app.route('/api/results/<int:scan_id>')
def api_results(scan_id):
    scan_result = ScanResult.query.get_or_404(scan_id)
    open_ports = OpenPort.query.filter_by(scan_id=scan_id).all()
    vulnerabilities = VulnerabilityFound.query.filter_by(scan_id=scan_id).all()
    
    # Sonuçları JSON formatına dönüştür
    result = {
        'scan_id': scan_result.id,
        'target': scan_result.target,
        'scan_type': scan_result.scan_type,
        'scan_date': scan_result.scan_date.isoformat(),
        'status': scan_result.status,
        'open_ports': [
            {
                'port': port.port_number,
                'service': port.service_name,
                'protocol': port.protocol,
                'state': port.state
            } for port in open_ports
        ],
        'vulnerabilities': [
            {
                'name': vuln.name,
                'severity': vuln.severity,
                'description': vuln.description
            } for vuln in vulnerabilities
        ]
    }
    
    return jsonify(result)

with app.app_context():
    # Modelleri içe aktar ve veritabanı tablolarını oluştur
    db.create_all()
