#!/usr/bin/env python3
"""
Test script untuk headless Radar Surabaya scraper
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from headless_radar_scraper import HeadlessRadarSurabayaScraper
import json

def test_scraper():
    """Test fungsi scraper"""
    print("=== TEST HEADLESS RADAR SURABAYA SCRAPER ===")
    
    scraper = HeadlessRadarSurabayaScraper()
    
    try:
        # Test dengan query pencarian
        search_query = "surabaya"
        print(f"Testing dengan query: {search_query}")
        print("Mohon tunggu... (Proses ini memakan waktu beberapa menit)")
        
        # Lakukan scraping
        news_data = scraper.scrape_news_complete(search_query, max_articles=3)
        
        if news_data:
            print(f"\n✅ BERHASIL! Ditemukan {len(news_data)} artikel")
            
            # Tampilkan hasil
            for i, news in enumerate(news_data, 1):
                print(f"\n{i}. {news['title']}")
                print(f"   Link: {news['link']}")
                print(f"   Author: {news['author']}")
                print(f"   Content: {news['content'][:100]}...")
            
            # Simpan hasil test
            with open('test_headless_results.json', 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Hasil test disimpan ke test_headless_results.json")
            return True
            
        else:
            print("❌ GAGAL! Tidak ada artikel ditemukan")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    success = test_scraper()
    if success:
        print("\n🎉 Test berhasil! Scraper siap digunakan.")
    else:
        print("\n💥 Test gagal! Periksa error di atas.")