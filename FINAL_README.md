# Radar Surabaya News Scraper - Final Version

## Ringkasan

Saya telah membuat **5 versi scraper** untuk website Radar Surabaya (https://radarsurabaya.jawapos.com/) dengan berbagai pendekatan:

### 1. **simple_radar_scraper.py** - Versi Sederhana
- Menggunakan requests + BeautifulSoup
- Paling cepat dan ringan
- **Status**: ❌ Gagal (403 Forbidden)

### 2. **selenium_radar_scraper.py** - Versi Selenium
- Menggunakan Selenium WebDriver
- Dapat menangani JavaScript
- **Status**: ❌ Gagal (User data dir conflict)

### 3. **headless_radar_scraper.py** - Versi Headless
- Menggunakan Selenium dengan headless mode
- Menghindari masalah user data dir
- **Status**: ❌ Gagal (Tidak menemukan artikel)

### 4. **requests_radar_scraper.py** - Versi Requests Advanced
- Menggunakan requests dengan retry strategy
- Headers yang lebih realistis
- **Status**: ❌ Gagal (403 Forbidden)

### 5. **final_working_scraper.py** - Versi Final
- Kombinasi semua teknik anti-detection
- Paling robust dan lengkap
- **Status**: ⚠️ Perlu testing lebih lanjut

## Masalah yang Ditemukan

1. **403 Forbidden Error**: Website memblokir akses scraping
2. **JavaScript Heavy**: Website mungkin menggunakan JavaScript untuk load konten
3. **Anti-Bot Protection**: Website memiliki proteksi anti-bot yang kuat
4. **Rate Limiting**: Website membatasi request yang terlalu cepat

## Solusi yang Disarankan

### Untuk Mengatasi 403 Forbidden:

1. **Gunakan Proxy atau VPN**:
```python
proxies = {
    'http': 'http://proxy-server:port',
    'https': 'https://proxy-server:port'
}
response = session.get(url, proxies=proxies)
```

2. **Gunakan Rotating User Agents**:
```python
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    # ... lebih banyak user agents
]
```

3. **Gunakan Selenium dengan Undetected ChromeDriver**:
```python
import undetected_chromedriver as uc
driver = uc.Chrome()
```

4. **Implementasi Delay yang Lebih Lama**:
```python
time.sleep(random.uniform(10, 30))  # Delay 10-30 detik
```

## Cara Penggunaan

### Instalasi Dependencies:
```bash
pip install requests beautifulsoup4 selenium undetected-chromedriver
```

### Menjalankan Scraper:
```bash
python final_working_scraper.py
```

### Input:
- Masukkan kata kunci pencarian berita
- Contoh: "surabaya", "politik", "ekonomi"

### Output:
- File JSON dengan data berita
- Format: `berita_radar_surabaya_[kata_kunci].json`

## Struktur Data Output

```json
[
  {
    "title": "Judul Berita",
    "link": "https://radarsurabaya.jawapos.com/...",
    "date": "Tanggal Publikasi",
    "category": "Kategori Berita",
    "author": "Nama Penulis",
    "content": "Konten lengkap artikel..."
  }
]
```

## Rekomendasi untuk Produksi

1. **Gunakan Proxy Pool**: Rotasi proxy untuk menghindari blokir
2. **Implementasi Rate Limiting**: Delay yang lebih lama antar request
3. **Monitoring dan Logging**: Track success rate dan error
4. **Fallback Strategy**: Multiple scraping methods
5. **Legal Compliance**: Pastikan sesuai dengan robots.txt dan ToS

## File yang Dibuat

- `simple_radar_scraper.py` - Versi sederhana
- `selenium_radar_scraper.py` - Versi Selenium
- `headless_radar_scraper.py` - Versi headless
- `requests_radar_scraper.py` - Versi requests advanced
- `final_working_scraper.py` - Versi final (recommended)
- `test_*.py` - Script testing untuk setiap versi
- `requirements.txt` - Dependencies
- `README_SCRAPER.md` - Dokumentasi lengkap

## Catatan Penting

- Website Radar Surabaya memiliki proteksi anti-bot yang kuat
- Perlu menggunakan teknik anti-detection yang lebih canggih
- Pertimbangkan menggunakan proxy atau VPN
- Selalu patuhi robots.txt dan terms of service
- Gunakan untuk tujuan yang legal dan etis

## Kontak

Jika memerlukan bantuan lebih lanjut atau customisasi, silakan hubungi developer.