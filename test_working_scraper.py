#!/usr/bin/env python3
"""
Test script untuk working Radar Surabaya scraper
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from working_radar_scraper import WorkingRadarSurabayaScraper
import json

def test_scraper():
    """Test fungsi scraper"""
    print("=== TEST WORKING RADAR SURABAYA SCRAPER ===")
    
    try:
        scraper = WorkingRadarSurabayaScraper()
        
        # Test dengan query pencarian
        search_query = "surabaya"
        print(f"Testing dengan query: {search_query}")
        
        # Lakukan scraping
        news_data = scraper.scrape_news_complete(search_query, max_articles=3)
        
        if news_data:
            print(f"\n✅ BERHASIL! Ditemukan {len(news_data)} artikel")
            
            # Tampilkan hasil
            for i, news in enumerate(news_data, 1):
                print(f"\n{i}. {news['title']}")
                print(f"   Link: {news['link']}")
                print(f"   Date: {news['date']}")
                print(f"   Category: {news['category']}")
                print(f"   Author: {news['author']}")
                print(f"   Content: {news['content'][:100]}...")
            
            # Simpan hasil test
            with open('working_test_results.json', 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Hasil test disimpan ke working_test_results.json")
            return True
            
        else:
            print("❌ GAGAL! Tidak ada artikel ditemukan")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    finally:
        try:
            scraper.close_driver()
        except:
            pass

if __name__ == "__main__":
    success = test_scraper()
    if success:
        print("\n🎉 Test berhasil! Scraper siap digunakan.")
    else:
        print("\n💥 Test gagal! Periksa error di atas.")