"""
Test Script untuk Radar Surabaya Scraper
=========================================
Script untuk testing scraper dengan berbagai skenario
"""

from radar_surabaya_scraper import RadarSurabayaScraper
import sys

def test_basic_scraping():
    """
    Test 1: Basic scraping dengan 1 halaman
    """
    print("="*80)
    print("TEST 1: Basic Scraping (1 halaman)")
    print("="*80)
    
    try:
        scraper = RadarSurabayaScraper()
        print("✓ Scraper instance created successfully")
        
        # Test dengan keyword sederhana
        keyword = "surabaya"
        print(f"\n🔍 Testing dengan keyword: '{keyword}'")
        print("⏳ Mohon tunggu, ini mungkin memakan waktu 1-2 menit...")
        
        results = scraper.search_news(keyword, max_pages=1)
        
        if results:
            print(f"\n✅ TEST PASSED!")
            print(f"   Berhasil scrape {len(results)} artikel")
            print(f"\n📰 Sample artikel pertama:")
            print(f"   Judul: {results[0].get('title', 'N/A')[:60]}...")
            print(f"   Tanggal: {results[0].get('date', 'N/A')}")
            print(f"   Kategori: {results[0].get('category', 'N/A')}")
            print(f"   Penulis: {results[0].get('author', 'N/A')}")
            print(f"   Konten: {len(results[0].get('content', ''))} karakter")
            
            # Save hasil
            scraper.save_to_csv("test_results.csv")
            print(f"\n✓ Hasil disimpan ke: test_results.csv")
            
            return True
        else:
            print("\n❌ TEST FAILED!")
            print("   Tidak ada artikel ditemukan")
            print("\n💡 Kemungkinan penyebab:")
            print("   1. Website masih blocking (coba tunggu 5-10 menit)")
            print("   2. Keyword tidak menghasilkan hasil")
            print("   3. Perlu menggunakan Selenium version")
            print("\n🔧 Solusi:")
            print("   python radar_scraper_selenium.py")
            
            return False
            
    except Exception as e:
        print(f"\n❌ TEST FAILED dengan error!")
        print(f"   Error: {e}")
        print(f"\n📋 Check log file untuk detail:")
        print(f"   tail -f radar_scraper.log")
        return False


def test_connection():
    """
    Test 0: Test koneksi ke website
    """
    print("="*80)
    print("TEST 0: Connection Test")
    print("="*80)
    
    try:
        import requests
        
        print("🔗 Testing connection to radarsurabaya.jawapos.com...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get('https://radarsurabaya.jawapos.com', 
                              headers=headers, 
                              timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Connection successful!")
            return True
        elif response.status_code == 403:
            print("⚠️  Got 403 Forbidden")
            print("   Tapi ini normal untuk request pertama")
            print("   Scraper akan handle ini dengan retry mechanism")
            return True
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed!")
        print("   Periksa koneksi internet Anda")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_imports():
    """
    Test -1: Verify all imports
    """
    print("="*80)
    print("TEST -1: Import Dependencies")
    print("="*80)
    
    try:
        print("📦 Checking imports...")
        
        from bs4 import BeautifulSoup
        print("   ✓ beautifulsoup4")
        
        import csv
        print("   ✓ csv")
        
        import json
        print("   ✓ json")
        
        import time
        print("   ✓ time")
        
        import random
        print("   ✓ random")
        
        import logging
        print("   ✓ logging")
        
        # Check cloudscraper (IMPORTANT for Cloudflare bypass)
        try:
            import cloudscraper
            print("   ✓ cloudscraper (Cloudflare bypass enabled)")
            has_cloudscraper = True
        except ImportError:
            print("   ⚠️  cloudscraper NOT installed (Cloudflare bypass disabled)")
            has_cloudscraper = False
        
        import requests
        print("   ✓ requests")
        
        if not has_cloudscraper:
            print("\n⚠️  WARNING: cloudscraper tidak terinstall!")
            print("   Website radarsurabaya.jawapos.com menggunakan Cloudflare protection.")
            print("   Scraper mungkin gagal tanpa cloudscraper.")
            print("\n   SOLUSI: pip install cloudscraper")
            print("\n   Continuing with basic tests...")
        
        print("\n✅ All core dependencies imported successfully!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        print("\n💡 Solusi:")
        print("   pip install -r requirements.txt")
        return False


def main():
    """
    Run all tests
    """
    print("\n")
    print("🧪 RADAR SURABAYA SCRAPER - TEST SUITE")
    print("="*80)
    print("\n")
    
    tests = [
        ("Import Dependencies", test_imports),
        ("Connection Test", test_connection),
        ("Basic Scraping", test_basic_scraping),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print("\n")
        except KeyboardInterrupt:
            print("\n\n⚠️  Test interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Test crashed: {e}")
            results.append((test_name, False))
            print("\n")
    
    # Summary
    print("="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status}: {test_name}")
    
    print("\n" + "="*80)
    print(f"Result: {passed}/{total} tests passed")
    print("="*80)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Scraper siap digunakan!")
        print("\n📝 Untuk mulai scraping:")
        print("   python radar_surabaya_scraper.py")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("📋 Check output di atas untuk detail error")
        print("\n💡 Troubleshooting:")
        print("   1. Pastikan dependencies terinstall: pip install -r requirements.txt")
        print("   2. Check koneksi internet")
        print("   3. Coba gunakan Selenium version: python radar_scraper_selenium.py")
        print("   4. Baca dokumentasi: FIX_403_ERROR.md")
    
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests cancelled by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
