/**
 * ZeroFind - Ana JavaScript Dosyası
 * made by wr4th0 (https://wr4thinfo.github.io)
 * Versiyon: 2.0 (2025)
 */

/**
 * Terminal modunu açma fonksiyonu
 */
function openTerminal() {
    // Terminal modunu başlatmak için Python betiğini çalıştır
    window.open('/terminal', 'ZeroFind Terminal', 'width=800,height=600,resizable=yes,scrollbars=yes');
    return false; // Link tıklamasını engelle
}

document.addEventListener('DOMContentLoaded', function() {
    // Form gönderimini yönet
    setupScanForm();
    
    // Zafiyet detay açılır panelleri
    setupVulnerabilityAccordions();
    
    // Aktif sayfayı işaretle
    highlightActivePage();
    
    // Eğer sonuç sayfasındaysa grafikler oluştur
    if (document.querySelector('#port-chart') || document.querySelector('#vulnerability-chart')) {
        setupResultCharts();
    }
    
    // Geçmiş sayfasında tablo sıralama
    if (document.querySelector('.scan-history-table')) {
        setupTableSorting();
    }
    
    // Toplu tarama modu toggle
    const enableBatchCheckbox = document.getElementById('enable_batch');
    const batchUploadDiv = document.getElementById('batch_upload');
    const targetInput = document.getElementById('target');
    
    if (enableBatchCheckbox && batchUploadDiv && targetInput) {
        enableBatchCheckbox.addEventListener('change', function() {
            if (this.checked) {
                batchUploadDiv.style.display = 'block';
                targetInput.placeholder = 'Toplu modda iken kullanılmaz';
                targetInput.disabled = true;
            } else {
                batchUploadDiv.style.display = 'none';
                targetInput.placeholder = 'örnek.com veya 192.168.1.1';
                targetInput.disabled = false;
            }
        });
    }
});

/**
 * Tarama formunu yönet
 */
function setupScanForm() {
    const scanForm = document.getElementById('scan-form');
    const resultSection = document.getElementById('scan-results-section');
    const scanningSection = document.getElementById('scanning-section');
    
    if (scanForm) {
        scanForm.addEventListener('submit', function(e) {
            // Form gönderimini normal işle, sadece kullanıcı deneyimi için UI'ı güncelle
            if (resultSection) resultSection.style.display = 'none';
            if (scanningSection) {
                scanningSection.style.display = 'block';
                scrollToElement(scanningSection);
            }
        });
    }
}

/**
 * Sonuç sayfasında zafiyet detay açılır panelleri
 */
function setupVulnerabilityAccordions() {
    const accordions = document.querySelectorAll('.vulnerability-accordion-header');
    
    // İlk zafiyeti varsayılan olarak açık göster (varsa)
    if (accordions.length > 0) {
        const firstContent = accordions[0].nextElementSibling;
        firstContent.style.maxHeight = firstContent.scrollHeight + "px";
        accordions[0].classList.add('active');
    }
    
    accordions.forEach(accordion => {
        accordion.addEventListener('click', function() {
            // Bu başlığa ait içerik panelini bul
            const content = this.nextElementSibling;
            
            // Açılır/kapanır durumu değiştir
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                this.classList.remove('active');
            } else {
                // Diğer tüm açık panelleri kapat (akordeon etkisi için)
                accordions.forEach(acc => {
                    if (acc !== this) {
                        acc.classList.remove('active');
                        acc.nextElementSibling.style.maxHeight = null;
                    }
                });
                
                // Bu paneli aç
                content.style.maxHeight = content.scrollHeight + "px";
                this.classList.add('active');
                
                // Görünüme getir
                setTimeout(() => {
                    this.scrollIntoView({behavior: 'smooth', block: 'center'});
                }, 300);
            }
        });
    });
}

/**
 * Aktif sayfa bağlantısını vurgula
 */
function highlightActivePage() {
    const navLinks = document.querySelectorAll('.nexus-nav a');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        
        if (currentPath === linkPath || 
            (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Sonuç sayfasında grafikleri oluştur
 */
function setupResultCharts() {
    // Port dağılımı grafiği
    const portChartElement = document.getElementById('port-chart');
    if (portChartElement) {
        createPortDistributionChart();
    }
    
    // Zafiyet dağılımı grafiği
    const vulnChartElement = document.getElementById('vulnerability-chart');
    if (vulnChartElement) {
        createVulnerabilityChart();
    }
}

/**
 * Port dağılımı grafiğini oluştur
 */
function createPortDistributionChart() {
    const ctx = document.getElementById('port-chart').getContext('2d');
    
    // Veriyi DOM'dan topla
    const portElements = document.querySelectorAll('.port-data');
    const ports = Array.from(portElements).map(el => el.dataset.port);
    const services = Array.from(portElements).map(el => el.dataset.service);
    
    // Servis gruplarını hesapla
    const serviceGroups = {};
    services.forEach(service => {
        if (serviceGroups[service]) {
            serviceGroups[service]++;
        } else {
            serviceGroups[service] = 1;
        }
    });
    
    // Grafik verilerini hazırla
    const serviceLabels = Object.keys(serviceGroups);
    const serviceCounts = Object.values(serviceGroups);
    
    // Renk paleti
    const colors = [
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 99, 132, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)',
        'rgba(199, 199, 199, 0.6)',
        'rgba(83, 102, 255, 0.6)',
        'rgba(40, 159, 64, 0.6)',
        'rgba(210, 199, 199, 0.6)',
    ];
    
    // Grafiği oluştur
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: serviceLabels,
            datasets: [{
                data: serviceCounts,
                backgroundColor: colors.slice(0, serviceLabels.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'Servis Dağılımı'
                }
            }
        }
    });
}

/**
 * Zafiyet dağılımı grafiğini oluştur
 */
function createVulnerabilityChart() {
    const ctx = document.getElementById('vulnerability-chart').getContext('2d');
    
    // Veriyi DOM'dan topla
    const vulnElements = document.querySelectorAll('.vulnerability-data');
    const severityCounts = {
        'düşük': 0,
        'orta': 0,
        'yüksek': 0,
        'kritik': 0
    };
    
    // Zafiyet sayılarını hesapla
    Array.from(vulnElements).forEach(el => {
        const severity = el.dataset.severity;
        if (severityCounts[severity] !== undefined) {
            severityCounts[severity]++;
        }
    });
    
    // Grafiği oluştur
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Düşük', 'Orta', 'Yüksek', 'Kritik'],
            datasets: [{
                label: 'Zafiyet Sayısı',
                data: [
                    severityCounts['düşük'],
                    severityCounts['orta'],
                    severityCounts['yüksek'],
                    severityCounts['kritik']
                ],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)', // düşük - mavi
                    'rgba(255, 206, 86, 0.6)', // orta - sarı
                    'rgba(255, 99, 132, 0.6)', // yüksek - kırmızı
                    'rgba(153, 0, 0, 0.6)'    // kritik - koyu kırmızı
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(153, 0, 0, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Zafiyet Dağılımı (Önem Derecesine Göre)'
                }
            }
        }
    });
}

/**
 * Geçmiş sayfasında tablo sıralama işlevleri
 */
function setupTableSorting() {
    const table = document.querySelector('.scan-history-table');
    const headers = table.querySelectorAll('th');
    
    headers.forEach(header => {
        header.addEventListener('click', function() {
            const column = this.dataset.column;
            const order = this.dataset.order || 'asc';
            
            // Tüm başlıkların sıralama durumunu temizle
            headers.forEach(h => h.dataset.order = '');
            
            // Bu başlığın sıralama durumunu güncelle
            this.dataset.order = order === 'asc' ? 'desc' : 'asc';
            
            // Tabloyu sırala
            sortTable(table, column, order);
        });
    });
}

/**
 * Tabloyu belirli bir sütuna göre sırala
 */
function sortTable(table, column, order) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Sıralanacak satırları karşılaştır
    const sortedRows = rows.sort((a, b) => {
        const aValue = a.querySelector(`td[data-column="${column}"]`).textContent.trim();
        const bValue = b.querySelector(`td[data-column="${column}"]`).textContent.trim();
        
        // Tarih sütunu için özel işlem
        if (column === 'date') {
            return order === 'asc' 
                ? new Date(aValue) - new Date(bValue)
                : new Date(bValue) - new Date(aValue);
        }
        
        // Normal metin karşılaştırması
        return order === 'asc'
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });
    
    // DOM'u güncelle
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}

/**
 * Belirli bir elemente kaydırma yap
 */
function scrollToElement(element) {
    window.scrollTo({
        top: element.offsetTop,
        behavior: 'smooth'
    });
}

/**
 * Tarama işlemi iptal et
 */
function cancelScan() {
    const scanningSection = document.getElementById('scanning-section');
    const resultSection = document.getElementById('scan-results-section');
    
    if (scanningSection) scanningSection.style.display = 'none';
    if (resultSection) resultSection.style.display = 'block';
    
    // Kullanıcıya bilgi ver
    alert('Tarama işlemi iptal edildi.');
}

/**
 * Tarama sonuçlarını dışa aktar
 */
function exportResults(format) {
    const scanId = document.getElementById('scan-id')?.value;
    
    if (!scanId) {
        alert('Dışa aktarılacak tarama bulunamadı.');
        return;
    }
    
    // API'dan sonuçları al
    fetch(`/api/results/${scanId}`)
        .then(response => response.json())
        .then(data => {
            let content = '';
            let filename = '';
            
            if (format === 'json') {
                content = JSON.stringify(data, null, 2);
                filename = `zerofind_scan_${scanId}.json`;
                downloadFile(content, filename, 'application/json');
            } 
            else if (format === 'txt') {
                // Düz metin raporu oluştur
                content = formatResultsAsText(data);
                filename = `zerofind_scan_${scanId}.txt`;
                downloadFile(content, filename, 'text/plain');
            }
        })
        .catch(error => {
            console.error('Dışa aktarma hatası:', error);
            alert('Sonuçlar dışa aktarılırken bir hata oluştu.');
        });
}

/**
 * Sonuçları düz metin formatında biçimlendir
 */
function formatResultsAsText(data) {
    const lines = [
        '============ ZEROFIND TARAMA RAPORU ============',
        '',
        `Tarama ID: ${data.scan_id}`,
        `Hedef: ${data.target}`,
        `Tarama Tipi: ${data.scan_type}`,
        `Tarama Tarihi: ${data.scan_date}`,
        `Durum: ${data.status}`,
        '',
        '--------------- AÇIK PORTLAR ---------------',
        ''
    ];
    
    // Açık portları ekle
    if (data.open_ports && data.open_ports.length > 0) {
        data.open_ports.forEach(port => {
            lines.push(`Port: ${port.port}/${port.protocol} - ${port.service} (${port.state})`);
        });
    } else {
        lines.push('Açık port bulunamadı.');
    }
    
    lines.push('');
    lines.push('--------------- GÜVENLİK AÇIKLARI ---------------');
    lines.push('');
    
    // Zafiyetleri ekle
    if (data.vulnerabilities && data.vulnerabilities.length > 0) {
        data.vulnerabilities.forEach(vuln => {
            lines.push(`Zafiyet: ${vuln.name}`);
            lines.push(`Önem Derecesi: ${vuln.severity}`);
            lines.push(`Açıklama: ${vuln.description}`);
            lines.push('');
        });
    } else {
        lines.push('Güvenlik açığı bulunamadı.');
    }
    
    return lines.join('\n');
}

/**
 * Dosya indirme
 */
function downloadFile(content, filename, contentType) {
    const a = document.createElement('a');
    const blob = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
