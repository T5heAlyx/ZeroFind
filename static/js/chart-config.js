/**
 * NexusGuard - Grafik Konfigürasyonu
 * Chart.js kütüphanesi için yapılandırma ve yardımcı fonksiyonlar
 */

// Grafik tema renkleri
const chartColors = {
    primary: 'rgb(0, 128, 128)',
    secondary: 'rgb(30, 136, 229)',
    success: 'rgb(67, 160, 71)',
    warning: 'rgb(255, 193, 7)',
    danger: 'rgb(229, 57, 53)',
    info: 'rgb(3, 155, 229)',
    dark: 'rgb(33, 33, 33)',
    grey: 'rgb(158, 158, 158)',
    
    // Zafiyet önem dereceleri için
    low: 'rgb(3, 155, 229)',      // info - mavi
    medium: 'rgb(255, 193, 7)',   // warning - sarı
    high: 'rgb(229, 57, 53)',     // danger - kırmızı
    critical: 'rgb(136, 14, 79)', // critical - bordo
    
    // Servis türleri için
    web: 'rgb(30, 136, 229)',      // http/https - mavi
    database: 'rgb(67, 160, 71)',  // mysql/pgsql - yeşil
    mail: 'rgb(255, 193, 7)',      // smtp/pop3 - sarı
    file: 'rgb(3, 155, 229)',      // ftp/sftp - açık mavi
    remote: 'rgb(229, 57, 53)',    // ssh/rdp - kırmızı
    dns: 'rgb(156, 39, 176)',      // dns - mor
    other: 'rgb(158, 158, 158)'    // diğer - gri
};

// Ortak grafik yapılandırması
const commonChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'right',
            labels: {
                font: {
                    family: "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif"
                }
            }
        },
        tooltip: {
            titleFont: {
                family: "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif"
            },
            bodyFont: {
                family: "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif"
            },
            padding: 12,
            backgroundColor: 'rgba(0, 0, 0, 0.8)'
        }
    }
};

/**
 * Servis tür grafiği oluşturma
 * @param {string} elementId - Grafik canvas element ID'si
 * @param {Object} data - Grafik verisi
 */
function createServiceTypeChart(elementId, data) {
    const ctx = document.getElementById(elementId).getContext('2d');
    
    // Servis türü renk eşleştirmeleri
    const serviceColorMap = {
        'http': chartColors.web,
        'https': chartColors.web,
        'mysql': chartColors.database,
        'postgresql': chartColors.database,
        'mongodb': chartColors.database,
        'smtp': chartColors.mail,
        'pop3': chartColors.mail,
        'imap': chartColors.mail,
        'ftp': chartColors.file,
        'sftp': chartColors.file,
        'ssh': chartColors.remote,
        'rdp': chartColors.remote,
        'dns': chartColors.dns,
        'domain': chartColors.dns
    };
    
    // Eşleşmeyen servisler için varsayılan renk
    const getServiceColor = (service) => {
        const serviceLower = service.toLowerCase();
        for (const [key, color] of Object.entries(serviceColorMap)) {
            if (serviceLower.includes(key)) {
                return color;
            }
        }
        return chartColors.other;
    };
    
    // Dinamik renk ataması
    const colors = data.labels.map(service => getServiceColor(service));
    
    // Pasta grafiği oluştur
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: colors,
                borderColor: 'white',
                borderWidth: 1
            }]
        },
        options: {
            ...commonChartOptions,
            plugins: {
                ...commonChartOptions.plugins,
                title: {
                    display: true,
                    text: 'Servis Türü Dağılımı',
                    font: {
                        size: 16,
                        family: "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif"
                    }
                }
            }
        }
    });
}

/**
 * Zafiyet önem grafiği oluşturma
 * @param {string} elementId - Grafik canvas element ID'si
 * @param {Object} data - Grafik verisi {düşük: x, orta: y, yüksek: z, kritik: w}
 */
function createVulnerabilitySeverityChart(elementId, data) {
    const ctx = document.getElementById(elementId).getContext('2d');
    
    // Türkçe etiketler
    const labels = ['Düşük', 'Orta', 'Yüksek', 'Kritik'];
    
    // İngilizce anahtarlar -> Türkçe anahtarlar
    const values = [
        data.düşük || data.low || 0,
        data.orta || data.medium || 0,
        data.yüksek || data.high || 0,
        data.kritik || data.critical || 0
    ];
    
    // Önem derecesi renkleri
    const backgroundColors = [
        chartColors.low,
        chartColors.medium,
        chartColors.high,
        chartColors.critical
    ];
    
    // Çubuk grafiği oluştur
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Zafiyet Sayısı',
                data: values,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color.replace('rgb', 'rgba').replace(')', ', 1)')),
                borderWidth: 1
            }]
        },
        options: {
            ...commonChartOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            },
            plugins: {
                ...commonChartOptions.plugins,
                title: {
                    display: true,
                    text: 'Güvenlik Açıkları (Önem Derecesine Göre)',
                    font: {
                        size: 16,
                        family: "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif"
                    }
                }
            }
        }
    });
}

/**
 * Zaman çizelgesi grafiği oluşturma
 * @param {string} elementId - Grafik canvas element ID'si
 * @param {Object} data - Tarih ve değerler {dates: [], values: []}
 * @param {string} title - Grafik başlığı
 */
function createTimelineChart(elementId, data, title) {
    const ctx = document.getElementById(elementId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Güvenlik Açığı Sayısı',
                data: data.values,
                backgroundColor: 'rgba(0, 128, 128, 0.2)',
                borderColor: chartColors.primary,
                borderWidth: 2,
                tension: 0.3,
                fill: true,
                pointBackgroundColor: chartColors.primary
            }]
        },
        options: {
            ...commonChartOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            },
            plugins: {
                ...commonChartOptions.plugins,
                title: {
                    display: true,
                    text: title || 'Zamanla Güvenlik Açıkları',
                    font: {
                        size: 16,
                        family: "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif"
                    }
                }
            }
        }
    });
}

/**
 * Port dağılımı grafiği oluşturma
 * @param {string} elementId - Grafik canvas element ID'si
 * @param {Array} portData - Port verisi [{port: x, count: y}, ...]
 */
function createPortDistributionChart(elementId, portData) {
    const ctx = document.getElementById(elementId).getContext('2d');
    
    // En yaygın 10 portu al, diğerlerini "Diğer" kategorisine topla
    const topPorts = [];
    let otherCount = 0;
    
    if (portData.length > 10) {
        // Sayılarına göre sırala
        portData.sort((a, b) => b.count - a.count);
        
        // İlk 9'u al
        topPorts.push(...portData.slice(0, 9));
        
        // Geriye kalanları topla
        for (let i = 9; i < portData.length; i++) {
            otherCount += portData[i].count;
        }
        
        // "Diğer" kategorisini ekle
        if (otherCount > 0) {
            topPorts.push({ port: 'Diğer', count: otherCount });
        }
    } else {
        topPorts.push(...portData);
    }
    
    // Grafik verilerini hazırla
    const labels = topPorts.map(item => `Port ${item.port}`);
    const data = topPorts.map(item => item.count);
    
    // Rastgele renkler oluştur
    const generateColors = (count) => {
        const colors = [];
        for (let i = 0; i < count; i++) {
            // Temel renklerden seçim yap
            const baseColors = [
                chartColors.primary,
                chartColors.secondary,
                chartColors.success,
                chartColors.danger,
                chartColors.warning,
                chartColors.info,
                'rgb(156, 39, 176)',
                'rgb(255, 87, 34)',
                'rgb(121, 85, 72)',
                'rgb(96, 125, 139)'
            ];
            
            if (i < baseColors.length) {
                colors.push(baseColors[i]);
            } else {
                // Benzersiz renkler oluştur
                const r = Math.floor(Math.random() * 200);
                const g = Math.floor(Math.random() * 200);
                const b = Math.floor(Math.random() * 200);
                colors.push(`rgb(${r}, ${g}, ${b})`);
            }
        }
        return colors;
    };
    
    const backgroundColors = generateColors(topPorts.length);
    
    // Çörek (doughnut) grafiği oluştur
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderColor: 'white',
                borderWidth: 1
            }]
        },
        options: {
            ...commonChartOptions,
            plugins: {
                ...commonChartOptions.plugins,
                title: {
                    display: true,
                    text: 'Açık Port Dağılımı',
                    font: {
                        size: 16,
                        family: "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif"
                    }
                }
            }
        }
    });
}

/**
 * DOM verilerinden grafik verisi oluştur
 * @param {string} selector - DOM element selector
 * @param {string} attribute - Veri özniteliği (data attribute)
 * @returns {Array} - Benzersiz değerler ve sayıları
 */
function getChartDataFromDOM(selector, attribute) {
    const elements = document.querySelectorAll(selector);
    const valueMap = {};
    
    elements.forEach(el => {
        const value = el.getAttribute(`data-${attribute}`);
        if (value) {
            valueMap[value] = (valueMap[value] || 0) + 1;
        }
    });
    
    return {
        labels: Object.keys(valueMap),
        values: Object.values(valueMap)
    };
}
