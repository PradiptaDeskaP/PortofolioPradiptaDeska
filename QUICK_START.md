# ⚡ Quick Start Guide - Radar Surabaya Scraper

## 🚀 Get Started in 3 Minutes!

### Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

**IMPORTANT:** Includes `cloudscraper` untuk bypass Cloudflare protection!

If you get Cloudflare errors, make sure cloudscraper is installed:
```bash
pip install cloudscraper
```

### Step 2: Run the Scraper (30 seconds)

```bash
python radar_surabaya_scraper.py
```

### Step 3: Enter Your Search (30 seconds)

When prompted:
- **Keyword**: Type your search term (example: "harga jagung")
- **Pages**: Enter number of pages (example: 5)
- **Output**: Choose format (CSV, JSON, or both)

### That's It! 🎉

Your scraped data will be saved automatically!

---

## 📝 Example Session

```bash
$ python radar_surabaya_scraper.py

================================================================================
RADAR SURABAYA NEWS SCRAPER
Scraper profesional untuk artikel berita Radar Surabaya
================================================================================

Masukkan keyword berita yang ingin Anda cari:
Contoh: harga jagung, pemilu, pendidikan, kesehatan, dll.
Keyword: harga jagung

Berapa halaman yang ingin di-scrape? (default: 5): 3

🚀 Memulai scraping untuk keyword: 'harga jagung' (maksimal 3 halaman)
Mohon tunggu, proses ini mungkin memakan waktu beberapa menit...

2025-11-06 10:30:15 - INFO - Memulai pencarian berita dengan keyword: 'harga jagung'
2025-11-06 10:30:16 - INFO - Scraping halaman 1: https://radarsurabaya.jawapos.com/search?q=harga+jagung
2025-11-06 10:30:18 - INFO - Ditemukan 10 artikel di halaman 1
...

================================================================================
RINGKASAN HASIL SCRAPING - Total: 25 artikel
================================================================================

[1] Harga Jagung Melonjak di Pasar Surabaya
    URL: https://radarsurabaya.jawapos.com/artikel/xxx
    Tanggal: 5 November 2025
    Kategori: Ekonomi
    Penulis: John Doe
    Konten: Harga jagung di berbagai pasar tradisional Surabaya mengalami...

...

================================================================================
MENYIMPAN HASIL
================================================================================

Pilih format output:
1. CSV
2. JSON
3. Keduanya
Pilihan (1/2/3, default: 3): 3

✓ Data berhasil disimpan ke: radar_surabaya_20251106_103045.csv
✓ Data berhasil disimpan ke: radar_surabaya_20251106_103045.json

================================================================================
✓ SCRAPING SELESAI!
✓ Total artikel berhasil di-scrape: 25
✓ Log tersimpan di: radar_scraper.log
================================================================================
```

---

## 🎯 Common Use Cases

### 1. Monitor Commodity Prices
```bash
python radar_surabaya_scraper.py
# Keyword: harga cabai
# Pages: 5
```

### 2. Track Political News
```bash
python radar_surabaya_scraper.py
# Keyword: pemilu 2024
# Pages: 10
```

### 3. Follow Education News
```bash
python radar_surabaya_scraper.py
# Keyword: pendidikan surabaya
# Pages: 3
```

---

## 🔧 Advanced Usage

### Use Python Script Directly

```python
from radar_surabaya_scraper import RadarSurabayaScraper

scraper = RadarSurabayaScraper()
results = scraper.search_news("teknologi", max_pages=5)
scraper.save_to_csv("my_results.csv")
```

### Run Examples

```bash
python example_usage.py
```

### Use Selenium Version (for dynamic content)

```bash
# Install additional dependencies first
pip install selenium webdriver-manager

# Run Selenium version
python radar_scraper_selenium.py
```

---

## ❓ Troubleshooting

### Problem: "ModuleNotFoundError"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Connection Timeout"
**Solution**: Check internet connection and try again

### Problem: "No Articles Found"
**Solution**: Try different keyword or check if website is accessible

---

## 📚 More Information

- Full documentation: [README_SCRAPER.md](README_SCRAPER.md)
- Examples: [example_usage.py](example_usage.py)
- Selenium version: [radar_scraper_selenium.py](radar_scraper_selenium.py)

---

## 💡 Tips

1. **Start Small**: Test with 1-2 pages first
2. **Be Patient**: Scraping takes time (1-2 minutes per page)
3. **Check Logs**: See `radar_scraper.log` for details
4. **Respect Rate Limits**: Don't scrape too frequently
5. **Use Meaningful Keywords**: More specific = better results

---

## 🌟 Features at a Glance

✅ **Easy to Use** - Just run and enter keyword  
✅ **Fast Setup** - Install in 1 minute  
✅ **Flexible Output** - CSV, JSON, or both  
✅ **Comprehensive Data** - Title, date, author, content  
✅ **Error Handling** - Robust and reliable  
✅ **Logging** - Track everything  
✅ **Professional Code** - Clean and maintainable  

---

**Happy Scraping! 🚀**

Questions? Check [README_SCRAPER.md](README_SCRAPER.md) for detailed documentation.
