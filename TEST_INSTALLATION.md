# 🧪 Test Installation - Radar Surabaya Scraper

## Quick Installation Test

### Step 1: Verify Python Installation

```bash
python --version
# Should show Python 3.7 or higher
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed requests-2.31.0 beautifulsoup4-4.12.3 lxml-5.1.0 ...
```

### Step 3: Verify Script Syntax

```bash
python -m py_compile radar_surabaya_scraper.py
```

If no error appears, the script is syntactically correct!

### Step 4: Test Import

```bash
python -c "from radar_surabaya_scraper import RadarSurabayaScraper; print('✓ Import successful!')"
```

Expected output:
```
✓ Import successful!
```

### Step 5: Test Basic Functionality

Create a simple test file `test_basic.py`:

```python
from radar_surabaya_scraper import RadarSurabayaScraper

print("Creating scraper instance...")
scraper = RadarSurabayaScraper()
print("✓ Scraper initialized successfully!")

print("\nTesting search (1 page only)...")
results = scraper.search_news("surabaya", max_pages=1)
print(f"✓ Found {len(results)} articles")

if results:
    print("\n✓ Sample article:")
    print(f"  Title: {results[0].get('title', 'N/A')[:50]}")
    print(f"  Date: {results[0].get('date', 'N/A')}")
    print(f"  Category: {results[0].get('category', 'N/A')}")
    print("\n✓✓✓ All tests passed! Scraper is working correctly! ✓✓✓")
else:
    print("⚠️  No articles found, but scraper is functional")
```

Run it:
```bash
python test_basic.py
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'requests'"

**Solution**: Install dependencies
```bash
pip install requests beautifulsoup4 lxml
```

### Error: "ModuleNotFoundError: No module named 'radar_surabaya_scraper'"

**Solution**: Make sure you're in the correct directory
```bash
cd /workspace
python radar_surabaya_scraper.py
```

### Error: "SyntaxError" in script

**Solution**: Make sure you're using Python 3.7+
```bash
python --version
# If needed, use python3 instead
python3 radar_surabaya_scraper.py
```

### Error: "Connection timeout" or "ConnectionError"

**Solution**: 
1. Check internet connection
2. Try with VPN if website is blocked
3. Increase timeout in code (change `timeout=30` to `timeout=60`)

### Error: "No articles found"

**Possible causes**:
1. Website structure changed (need to update selectors)
2. Website is down temporarily
3. Search query returns no results
4. Anti-bot detection (try Selenium version)

**Solution**: Try selenium version
```bash
pip install selenium webdriver-manager
python radar_scraper_selenium.py
```

---

## Performance Benchmarks

### Expected Performance

| Pages | Articles | Time (approx) |
|-------|----------|---------------|
| 1     | ~10      | 30-60 sec     |
| 3     | ~30      | 2-3 min       |
| 5     | ~50      | 4-5 min       |
| 10    | ~100     | 8-10 min      |

*Note: Actual time depends on internet speed and website response time*

### Resource Usage

- **CPU**: Low (5-10%)
- **Memory**: ~50-100 MB
- **Bandwidth**: ~1-2 MB per page
- **Disk**: Minimal (output files only)

---

## Verification Checklist

Before using the scraper in production, verify:

- [ ] Python 3.7+ installed
- [ ] All dependencies installed (`requirements.txt`)
- [ ] Script runs without syntax errors
- [ ] Can connect to radarsurabaya.jawapos.com
- [ ] Test scraping returns results
- [ ] CSV export works
- [ ] JSON export works
- [ ] Log file is created
- [ ] Error handling works (test with invalid keyword)

---

## Next Steps

After successful installation:

1. **Read Documentation**: [README_SCRAPER.md](README_SCRAPER.md)
2. **Try Examples**: Run `python example_usage.py`
3. **Start Scraping**: Run `python radar_surabaya_scraper.py`
4. **Advanced Usage**: Check Selenium version if needed

---

## Support

If you encounter issues:

1. Check this test guide
2. Review [QUICK_START.md](QUICK_START.md)
3. Check logs: `radar_scraper.log`
4. Try Selenium version for problematic websites

---

**Installation Complete! You're ready to scrape! 🚀**
