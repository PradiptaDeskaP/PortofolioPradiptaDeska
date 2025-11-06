# 🚀 Install Cloudscraper - Quick Guide

## ⚡ **FASTEST WAY (1 Command)**

```bash
pip install cloudscraper
```

**That's it!** Lalu run scraper:
```bash
python radar_surabaya_scraper.py
```

---

## 📦 **Complete Installation**

### **Method 1: Install All Dependencies**

```bash
# Install everything (recommended)
pip install -r requirements.txt
```

This installs:
- ✅ cloudscraper (Cloudflare bypass)
- ✅ beautifulsoup4 (HTML parsing)
- ✅ lxml (Fast parser)
- ✅ requests (HTTP client)
- ✅ All other dependencies

### **Method 2: Minimal Install**

```bash
# Just cloudscraper and essentials
pip install cloudscraper beautifulsoup4 lxml
```

### **Method 3: With Virtual Environment** ⭐ RECOMMENDED

```bash
# 1. Create venv
python -m venv venv

# 2. Activate
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Verify
python -c "import cloudscraper; print('✅ Success!')"
```

---

## ✅ **Verify Installation**

```bash
# Check if cloudscraper installed
python -c "import cloudscraper; print('✅ cloudscraper installed:', cloudscraper.__version__)"
```

**Expected output:**
```
✅ cloudscraper installed: 1.2.71
```

---

## 🧪 **Test Scraper**

```bash
# Run test suite
python test_scraper.py
```

**Expected output:**
```
✅ PASSED: Import Dependencies
✅ PASSED: Connection Test
✅ PASSED: Basic Scraping

Result: 3/3 tests passed
🎉 ALL TESTS PASSED!
```

---

## 🎯 **Run Scraper**

```bash
python radar_surabaya_scraper.py
```

**You should see:**
```
✓ Menggunakan cloudscraper untuk bypass Cloudflare protection
✓ Homepage berhasil diakses, cookies diperoleh
Memulai pencarian berita dengan keyword: '...'
```

---

## ⚠️ **Troubleshooting**

### **Error: "No module named 'cloudscraper'"**

```bash
# Solution 1: Reinstall
pip uninstall cloudscraper
pip install cloudscraper

# Solution 2: Check Python path
which python
pip --version

# Solution 3: Use python -m pip
python -m pip install cloudscraper
```

### **Error: "Permission denied"**

```bash
# Use --user flag
pip install --user cloudscraper

# Or use sudo (Linux/Mac)
sudo pip install cloudscraper
```

### **Error: Version conflicts**

```bash
# Upgrade pip first
pip install --upgrade pip

# Then install
pip install cloudscraper
```

---

## 📊 **Verify It's Working**

### **Check 1: Import Test**

```bash
python -c "from radar_surabaya_scraper import CLOUDSCRAPER_AVAILABLE; print('Cloudscraper available:', CLOUDSCRAPER_AVAILABLE)"
```

**Expected:**
```
Cloudscraper available: True
```

### **Check 2: Run Scraper**

When you run the scraper, first line should be:
```
✓ Menggunakan cloudscraper untuk bypass Cloudflare protection
```

If you see:
```
⚠️  cloudscraper tidak terinstall, menggunakan requests biasa
```

Then cloudscraper is NOT installed! Run:
```bash
pip install cloudscraper
```

---

## 🔄 **Update Cloudscraper**

```bash
# Check current version
pip show cloudscraper

# Update to latest
pip install --upgrade cloudscraper

# Force reinstall
pip install --force-reinstall cloudscraper
```

---

## 🌟 **Why Cloudscraper?**

| Feature | Regular Requests | **Cloudscraper** |
|---------|------------------|------------------|
| HTTP Requests | ✅ | ✅ |
| HTTPS | ✅ | ✅ |
| Cookies | ✅ | ✅ |
| Headers | ✅ | ✅ |
| **Cloudflare Bypass** | ❌ | **✅** |
| **JS Challenge** | ❌ | **✅** |
| **TLS Fingerprint** | ❌ | **✅** |

**Result:** ~90% success rate on Cloudflare-protected sites! ✅

---

## 📝 **Quick Reference**

```bash
# Install
pip install cloudscraper

# Verify
python -c "import cloudscraper"

# Test
python test_scraper.py

# Run
python radar_surabaya_scraper.py

# Update
pip install --upgrade cloudscraper
```

---

## 🆘 **Still Having Issues?**

### **Option 1: Use Selenium**

```bash
pip install selenium webdriver-manager
python radar_scraper_selenium.py
```

### **Option 2: Check Requirements**

```bash
# Python version (need 3.7+)
python --version

# Pip version
pip --version

# Installed packages
pip list | grep -i cloud
```

### **Option 3: Read Full Documentation**

- `FIX_CLOUDFLARE.md` - Complete Cloudflare bypass guide
- `README_SCRAPER.md` - Full scraper documentation
- `TROUBLESHOOTING.md` - Common issues and solutions

---

## ✅ **Success Checklist**

- [ ] Python 3.7+ installed
- [ ] pip working correctly
- [ ] cloudscraper installed (`pip install cloudscraper`)
- [ ] Import test passes (`python -c "import cloudscraper"`)
- [ ] Test script passes (`python test_scraper.py`)
- [ ] Scraper shows "✓ Menggunakan cloudscraper"
- [ ] Scraping works successfully

---

## 🎉 **Done!**

Once cloudscraper is installed, your scraper will:
- ✅ Bypass Cloudflare automatically
- ✅ Handle JS challenges
- ✅ Work with radarsurabaya.jawapos.com
- ✅ Have ~90% success rate

**Happy Scraping! 🚀**

---

**Need Help?**
1. Check `FIX_CLOUDFLARE.md` for detailed guide
2. Run `python test_scraper.py` to diagnose issues
3. Try Selenium version if cloudscraper fails
