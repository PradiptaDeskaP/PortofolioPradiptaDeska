# 🚀 Quick Start Guide - Tribunnews Scraper

## Instalasi Cepat (3 Langkah)

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Jalankan Scraper

```bash
python tribunnews_scraper.py
```

### 3️⃣ Input Keyword

```
Keyword: jagung
Jumlah halaman [3]: 2
Maksimal artikel [semua]: 10
```

**✅ Selesai!** File CSV dan JSON akan tersimpan otomatis.

---

## 📝 Contoh Cepat

### Scraping Berita "Harga Jagung"

```bash
$ python tribunnews_scraper.py
Keyword: harga jagung
Jumlah halaman [3]: 1
Maksimal artikel [semua]: 5
```

**Output:**
- `tribunnews_2025-11-08_14-30-45.csv`
- `tribunnews_2025-11-08_14-30-45.json`

### Menggunakan sebagai Module

```python
from tribunnews_scraper import TribunnewsScraper

scraper = TribunnewsScraper()
results = scraper.scrape_articles("jagung", max_pages=2, max_articles=10)
scraper.save_to_csv("hasil_jagung.csv")
```

---

## 🎯 Tips Cepat

| Kebutuhan | Recommended Setting |
|-----------|---------------------|
| Testing | max_pages=1, max_articles=5 |
| Quick Analysis | max_pages=2, max_articles=20 |
| Deep Research | max_pages=5, max_articles=50+ |
| Production | max_pages=10, max_articles=None |

---

## 🐛 Troubleshooting Cepat

**Error: Module not found**
```bash
pip install requests beautifulsoup4 lxml pandas
```

**Error: Timeout**
- Check internet connection
- Try again later

**Hasil kosong**
- Coba keyword lain yang lebih umum
- Check website masih online

---

## 📊 Output Format

**CSV Columns:**
- no, keyword, title, url
- publish_date, author, editor
- content, scraped_at

**Contoh Data:**

| no | keyword | title | publish_date | author |
|----|---------|-------|--------------|--------|
| 1 | jagung | Harga Jagung Naik... | Senin, 3 Nov 2025 | John Doe |
| 2 | jagung | Petani Keluhkan... | Selasa, 4 Nov 2025 | Jane Smith |

---

## 📚 Dokumentasi Lengkap

Lihat **README_SCRAPER.md** untuk dokumentasi lengkap dan advanced usage.

---

**Happy Scraping! 🎉**
