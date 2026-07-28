"""
Test Script Sederhana untuk Tribunnews Scraper
Script ini melakukan test scraping dengan jumlah data minimal
"""

from tribunnews_scraper import TribunnewsScraper
import sys


def test_basic_scraping():
    """
    Test scraping dasar dengan 2 artikel saja
    """
    print("\n" + "="*80)
    print("🧪 TEST SCRAPING TRIBUNNEWS")
    print("="*80)
    print("\n📝 Test Configuration:")
    print("   Keyword: surabaya")
    print("   Max Pages: 1")
    print("   Max Articles: 2")
    print("\n" + "="*80)
    
    try:
        # Inisialisasi scraper
        scraper = TribunnewsScraper()
        
        # Test scraping dengan minimal data
        print("\n🚀 Memulai test scraping...")
        results = scraper.scrape_articles(
            keyword="surabaya",
            max_pages=1,
            max_articles=2
        )
        
        # Validasi hasil
        if not results:
            print("\n❌ TEST GAGAL: Tidak ada hasil scraping")
            return False
        
        print(f"\n✅ Berhasil scrape {len(results)} artikel")
        
        # Validasi struktur data
        required_keys = ['no', 'keyword', 'title', 'url', 'publish_date', 
                        'author', 'editor', 'content', 'scraped_at']
        
        first_article = results[0]
        missing_keys = [key for key in required_keys if key not in first_article]
        
        if missing_keys:
            print(f"\n⚠️  WARNING: Missing keys: {missing_keys}")
        else:
            print("\n✅ Struktur data valid")
        
        # Tampilkan sample data
        print("\n📊 Sample Data (Artikel Pertama):")
        print("-" * 80)
        print(f"   Judul    : {first_article['title'][:60]}...")
        print(f"   URL      : {first_article['url']}")
        print(f"   Tanggal  : {first_article['publish_date']}")
        print(f"   Penulis  : {first_article['author']}")
        print(f"   Editor   : {first_article['editor']}")
        print(f"   Konten   : {len(first_article['content'])} karakter")
        print(f"   Scraped  : {first_article['scraped_at']}")
        
        # Test save to files
        print("\n💾 Test saving files...")
        scraper.save_to_csv("test_result.csv")
        scraper.save_to_json("test_result.json")
        
        # Tampilkan ringkasan
        scraper.display_summary()
        
        print("\n" + "="*80)
        print("✅ TEST BERHASIL!")
        print("="*80)
        print("\n📁 File yang dibuat:")
        print("   - test_result.csv")
        print("   - test_result.json")
        print("\n💡 Tip: Cek file tersebut untuk melihat hasil scraping")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST GAGAL: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    Main function untuk menjalankan test
    """
    print("\n🧪 Tribunnews Scraper - Test Script")
    print("Script ini akan melakukan test scraping dengan 2 artikel")
    print("Estimasi waktu: ~15-20 detik")
    
    input("\n⏎ Tekan ENTER untuk memulai test...")
    
    success = test_basic_scraping()
    
    if success:
        print("\n✅ Test selesai dengan sukses!")
        print("Anda dapat menggunakan scraper dengan menjalankan:")
        print("   python tribunnews_scraper.py")
        sys.exit(0)
    else:
        print("\n❌ Test gagal. Periksa error di atas.")
        sys.exit(1)


if __name__ == "__main__":
    main()
