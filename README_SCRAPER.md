# 🗞️ Radar Surabaya News Scraper

**Professional web scraper untuk mengambil artikel berita dari Radar Surabaya**

Dibuat oleh Data Engineer & AI Engineer profesional dengan pendekatan best practices dalam web scraping.

---

## 📋 Fitur Utama

✅ **Search Otomatis** - Cari berita berdasarkan keyword apapun  
✅ **Multi-page Scraping** - Scrape hingga 20 halaman hasil pencarian  
✅ **Data Lengkap** - Ambil judul, tanggal, kategori, penulis, dan konten lengkap  
✅ **Multiple Export** - Simpan hasil dalam format CSV dan JSON  
✅ **Error Handling** - Robust error handling dan retry mechanism  
✅ **Logging System** - Comprehensive logging untuk debugging  
✅ **Rate Limiting** - Built-in delays untuk menghindari blocking  
✅ **Clean Code** - Kode yang modular, maintainable, dan well-documented  

---

## 🚀 Instalasi

### 1. Clone atau Download Repository

```bash
cd /workspace
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verifikasi Instalasi

```bash
python radar_surabaya_scraper.py --help
```

---

## 💻 Cara Penggunaan

### Metode 1: Interactive Mode (Recommended untuk Pemula)

Jalankan script dan ikuti instruksi interaktif:

```bash
python radar_surabaya_scraper.py
```

Program akan meminta:
1. **Keyword** berita yang ingin dicari (contoh: "harga jagung", "pemilu", "pendidikan")
2. **Jumlah halaman** yang ingin di-scrape (1-20 halaman)
3. **Format output** yang diinginkan (CSV, JSON, atau keduanya)

### Metode 2: Programmatic Usage

Anda juga bisa menggunakan scraper dalam kode Python Anda sendiri:

```python
from radar_surabaya_scraper import RadarSurabayaScraper

# Inisialisasi scraper
scraper = RadarSurabayaScraper()

# Scrape berita
results = scraper.search_news("harga jagung", max_pages=3)

# Tampilkan hasil
scraper.print_summary()

# Simpan hasil
scraper.save_to_csv("hasil_scraping.csv")
scraper.save_to_json("hasil_scraping.json")
```

---

## 📊 Output Data

### Format CSV
File CSV akan berisi kolom berikut:
- `title` - Judul artikel
- `url` - URL artikel lengkap
- `date` - Tanggal publikasi
- `category` - Kategori berita
- `author` - Penulis artikel
- `excerpt` - Cuplikan artikel
- `content` - Konten lengkap artikel (text only)
- `published_datetime` - Timestamp publikasi (jika tersedia)

### Format JSON
File JSON akan berisi array of objects dengan struktur yang sama.

---

## 🔍 Contoh Penggunaan

### Contoh 1: Scrape Berita Harga Komoditas

```bash
python radar_surabaya_scraper.py
# Input: harga jagung
# Pages: 5
# Output: CSV dan JSON
```

### Contoh 2: Scrape Berita Politik

```bash
python radar_surabaya_scraper.py
# Input: pemilu 2024
# Pages: 10
# Output: JSON only
```

### Contoh 3: Monitoring Berita Terkini

```bash
python radar_surabaya_scraper.py
# Input: breaking news
# Pages: 1
# Output: CSV
```

---

## 🛠️ Troubleshooting

### Problem: "Connection Error" atau Timeout

**Solusi:**
1. Periksa koneksi internet Anda
2. Website mungkin sedang down, coba lagi nanti
3. Tingkatkan timeout di code (ubah `timeout=30` menjadi `timeout=60`)

### Problem: "No Articles Found"

**Solusi:**
1. Coba dengan keyword yang berbeda
2. Periksa apakah website Radar Surabaya dapat diakses di browser
3. Website mungkin mengubah struktur HTML (perlu update selector)

### Problem: "Scraping Terlalu Lambat"

**Solusi:**
1. Kurangi jumlah halaman yang di-scrape
2. Kurangi delay di code (ubah `time.sleep()` values)
3. Gunakan koneksi internet yang lebih cepat

### Problem: Data Tidak Lengkap

**Solusi:**
1. Beberapa artikel mungkin tidak memiliki author
2. Beberapa artikel mungkin memiliki format berbeda
3. Periksa log file (`radar_scraper.log`) untuk detail error

---

## 📈 Best Practices

### 1. **Gunakan Rate Limiting**
Jangan scrape terlalu cepat untuk menghindari IP blocking:
- Default delay: 1 detik antar artikel, 2 detik antar halaman
- Bisa disesuaikan di code (`time.sleep()`)

### 2. **Respect robots.txt**
Periksa file robots.txt website sebelum scraping massal:
```
https://radarsurabaya.jawapos.com/robots.txt
```

### 3. **Error Handling**
Script sudah dilengkapi error handling, tapi tetap monitor log file untuk memastikan tidak ada masalah.

### 4. **Data Storage**
- Untuk dataset kecil: gunakan CSV
- Untuk dataset besar atau analisis lanjutan: gunakan JSON atau database

### 5. **Legal Compliance**
- Scraping untuk personal research/education: ✅ OK
- Scraping untuk commercial use: ⚠️ Perlu izin dari pemilik website
- Selalu baca Terms of Service website

---

## 🔧 Konfigurasi Advanced

### Mengubah User Agent

Edit di `RadarSurabayaScraper.__init__()`:

```python
self.session.headers.update({
    'User-Agent': 'Your Custom User Agent Here'
})
```

### Menambah Delay

Edit nilai `time.sleep()` di method `search_news()`:

```python
time.sleep(2)  # Delay antar artikel (default: 1 detik)
time.sleep(5)  # Delay antar halaman (default: 2 detik)
```

### Custom Selector

Jika struktur website berubah, update selector di method:
- `_extract_search_results()` - untuk halaman pencarian
- `_scrape_article_detail()` - untuk halaman detail artikel

---

## 📁 Struktur File

```
/workspace/
├── radar_surabaya_scraper.py      # Main scraper script
├── requirements.txt                # Python dependencies
├── README_SCRAPER.md              # Dokumentasi (file ini)
├── radar_scraper.log              # Log file (auto-generated)
├── radar_surabaya_YYYYMMDD_HHMMSS.csv   # Output CSV (auto-generated)
└── radar_surabaya_YYYYMMDD_HHMMSS.json  # Output JSON (auto-generated)
```

---

## 🎯 Roadmap & Future Improvements

- [ ] Selenium support untuk dynamic content
- [ ] Database integration (MongoDB, PostgreSQL)
- [ ] Multi-threading untuk scraping lebih cepat
- [ ] Proxy rotation untuk scraping massal
- [ ] GUI Interface dengan Streamlit/Gradio
- [ ] Scheduled scraping dengan cron jobs
- [ ] Email notification untuk berita baru
- [ ] Sentiment analysis integration
- [ ] Automatic translation

---

## 📞 Support & Contact

Jika ada pertanyaan atau masalah:
1. Periksa log file: `radar_scraper.log`
2. Baca troubleshooting guide di atas
3. Update dependencies: `pip install -r requirements.txt --upgrade`

---

## ⚖️ Legal Disclaimer

Script ini dibuat untuk tujuan **edukasi dan penelitian**. Pengguna bertanggung jawab untuk:
- Mematuhi Terms of Service website target
- Tidak melakukan scraping yang berlebihan
- Tidak menggunakan data untuk tujuan ilegal
- Menghormati hak cipta konten

**Disclaimer**: Penulis tidak bertanggung jawab atas penyalahgunaan script ini.

---

## 🌟 Credits

Dibuat dengan ❤️ oleh Data Engineer & AI Engineer profesional

**Tech Stack:**
- Python 3.8+
- Requests & BeautifulSoup4
- CSV & JSON libraries
- Logging & Error Handling

---

## 📝 Changelog

### Version 1.0.0 (2025-11-06)
- ✅ Initial release
- ✅ Basic scraping functionality
- ✅ CSV and JSON export
- ✅ Multi-page support
- ✅ Comprehensive logging
- ✅ Error handling
- ✅ Interactive CLI

---

**Happy Scraping! 🚀**
