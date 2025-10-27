# Radar Surabaya News Scraper

Web scraper untuk mengambil berita dari website Radar Surabaya (https://radarsurabaya.jawapos.com/).

## Fitur

- ✅ Pencarian berita berdasarkan kata kunci
- ✅ Scraping judul, link, penulis, dan konten artikel
- ✅ Multiple fallback methods untuk memastikan scraping berhasil
- ✅ Export hasil ke file JSON
- ✅ Error handling yang komprehensif
- ✅ Rate limiting untuk menghindari blokir

## Instalasi

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download ChromeDriver:
   - Download dari: https://chromedriver.chromium.org/
   - Pastikan versi ChromeDriver sesuai dengan versi Chrome yang terinstall
   - Letakkan ChromeDriver di PATH atau di folder yang sama dengan script

## Penggunaan

### 1. Simple Scraper (Recommended)
Menggunakan requests + BeautifulSoup, lebih cepat dan reliable:

```bash
python simple_radar_scraper.py
```

### 2. Selenium Scraper
Menggunakan Selenium untuk JavaScript-heavy websites:

```bash
python selenium_radar_scraper.py
```

### 3. Advanced Scraper
Kombinasi requests + Selenium dengan fallback:

```bash
python radar_surabaya_scraper.py
```

### 4. Test Scraper
Jalankan test untuk memverifikasi scraper bekerja:

```bash
python test_scraper.py
```

## Output

Hasil scraping akan disimpan dalam format JSON dengan struktur:

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

## Troubleshooting

### Error: "ChromeDriver not found"
- Download ChromeDriver dan pastikan ada di PATH
- Atau letakkan ChromeDriver.exe di folder yang sama dengan script

### Error: "No articles found"
- Website mungkin menggunakan JavaScript untuk load content
- Coba gunakan selenium_radar_scraper.py
- Periksa koneksi internet

### Error: "Rate limited"
- Tambahkan delay lebih lama di kode
- Gunakan proxy atau VPN

## Struktur File

```
├── simple_radar_scraper.py      # Scraper sederhana (recommended)
├── selenium_radar_scraper.py    # Scraper dengan Selenium
├── radar_surabaya_scraper.py    # Scraper advanced
├── test_scraper.py              # Script test
├── requirements.txt             # Dependencies
└── README_SCRAPER.md           # Dokumentasi ini
```

## Catatan Penting

1. **Respect robots.txt**: Pastikan website mengizinkan scraping
2. **Rate limiting**: Jangan terlalu sering request untuk menghindari blokir
3. **Legal compliance**: Gunakan hanya untuk tujuan yang legal
4. **Website changes**: Struktur website bisa berubah, update selector jika perlu

## Support

Jika mengalami masalah:
1. Jalankan test_scraper.py untuk diagnosis
2. Periksa log error untuk detail masalah
3. Pastikan dependencies terinstall dengan benar
4. Cek koneksi internet dan akses ke website