"""
Contoh Penggunaan Tribunnews Scraper
Script ini menunjukkan berbagai cara menggunakan TribunnewsScraper
"""

from tribunnews_scraper import TribunnewsScraper
import time


def example_1_basic_scraping():
    """
    Contoh 1: Scraping dasar dengan satu keyword
    """
    print("\n" + "="*80)
    print("CONTOH 1: SCRAPING DASAR")
    print("="*80)
    
    scraper = TribunnewsScraper()
    
    # Scraping berita tentang "jagung"
    results = scraper.scrape_articles(
        keyword="jagung",
        max_pages=2,
        max_articles=10
    )
    
    # Simpan hasil
    scraper.save_to_csv("contoh_jagung.csv")
    scraper.save_to_json("contoh_jagung.json")
    
    # Tampilkan ringkasan
    scraper.display_summary()


def example_2_multiple_keywords():
    """
    Contoh 2: Scraping multiple keywords
    """
    print("\n" + "="*80)
    print("CONTOH 2: SCRAPING MULTIPLE KEYWORDS")
    print("="*80)
    
    keywords = ["harga jagung", "inflasi", "pangan"]
    
    for keyword in keywords:
        print(f"\n🔍 Processing keyword: {keyword}")
        
        scraper = TribunnewsScraper()
        results = scraper.scrape_articles(
            keyword=keyword,
            max_pages=1,
            max_articles=5
        )
        
        if results:
            # Simpan dengan nama file custom
            safe_keyword = keyword.replace(' ', '_').replace('/', '_')
            scraper.save_to_csv(f"berita_{safe_keyword}.csv")
            print(f"✅ Selesai: {len(results)} artikel untuk '{keyword}'")
        
        # Delay antar keyword
        time.sleep(5)


def example_3_filtered_scraping():
    """
    Contoh 3: Scraping dengan filter dan analisis
    """
    print("\n" + "="*80)
    print("CONTOH 3: SCRAPING DENGAN FILTER")
    print("="*80)
    
    scraper = TribunnewsScraper()
    results = scraper.scrape_articles(
        keyword="ekonomi",
        max_pages=2,
        max_articles=20
    )
    
    if results:
        # Filter artikel berdasarkan panjang konten
        long_articles = [r for r in results if len(r['content']) > 1000]
        print(f"\n📊 Artikel panjang (>1000 karakter): {len(long_articles)}")
        
        # Filter artikel berdasarkan penulis tertentu
        authors = {}
        for article in results:
            author = article['author']
            if author:
                authors[author] = authors.get(author, 0) + 1
        
        print(f"\n👥 Distribusi Penulis:")
        for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {author}: {count} artikel")
        
        scraper.save_to_csv("ekonomi_filtered.csv")


def example_4_accessing_results():
    """
    Contoh 4: Mengakses dan memproses hasil scraping
    """
    print("\n" + "="*80)
    print("CONTOH 4: MENGAKSES HASIL SCRAPING")
    print("="*80)
    
    scraper = TribunnewsScraper()
    results = scraper.scrape_articles(
        keyword="pertanian",
        max_pages=1,
        max_articles=5
    )
    
    # Akses setiap artikel
    for article in results:
        print(f"\n📰 {article['title']}")
        print(f"   📅 {article['publish_date']}")
        print(f"   ✍️  Penulis: {article['author']}")
        print(f"   📝 Konten: {len(article['content'])} karakter")
        print(f"   🔗 {article['url']}")


def example_5_error_handling():
    """
    Contoh 5: Error handling yang proper
    """
    print("\n" + "="*80)
    print("CONTOH 5: ERROR HANDLING")
    print("="*80)
    
    scraper = TribunnewsScraper()
    
    try:
        results = scraper.scrape_articles(
            keyword="test123xyz",  # Keyword yang mungkin tidak ada hasil
            max_pages=1,
            max_articles=5
        )
        
        if not results:
            print("⚠️  Tidak ada hasil, coba keyword lain")
        else:
            scraper.save_to_csv("test_results.csv")
            print(f"✅ Berhasil scrape {len(results)} artikel")
            
    except Exception as e:
        print(f"❌ Error terjadi: {str(e)}")
        print("Melanjutkan ke keyword berikutnya...")


def example_6_custom_filename():
    """
    Contoh 6: Custom filename untuk output
    """
    print("\n" + "="*80)
    print("CONTOH 6: CUSTOM FILENAME")
    print("="*80)
    
    scraper = TribunnewsScraper()
    results = scraper.scrape_articles(
        keyword="surabaya",
        max_pages=1,
        max_articles=5
    )
    
    if results:
        # Simpan dengan nama file custom
        scraper.save_to_csv("surabaya_berita_terbaru.csv")
        scraper.save_to_json("surabaya_berita_terbaru.json")
        print("✅ File disimpan dengan nama custom")


def example_7_batch_scraping():
    """
    Contoh 7: Batch scraping dengan progress tracking
    """
    print("\n" + "="*80)
    print("CONTOH 7: BATCH SCRAPING")
    print("="*80)
    
    keywords = [
        "harga pangan",
        "inflasi surabaya",
        "UMKM",
        "wisata surabaya",
        "pendidikan"
    ]
    
    all_results = []
    
    for idx, keyword in enumerate(keywords, 1):
        print(f"\n[{idx}/{len(keywords)}] Scraping: {keyword}")
        
        scraper = TribunnewsScraper()
        results = scraper.scrape_articles(
            keyword=keyword,
            max_pages=1,
            max_articles=3
        )
        
        all_results.extend(results)
        
        # Delay antar batch
        if idx < len(keywords):
            time.sleep(5)
    
    # Simpan semua hasil dalam satu file
    if all_results:
        import pandas as pd
        df = pd.DataFrame(all_results)
        df.to_csv("batch_all_keywords.csv", index=False, encoding='utf-8-sig')
        print(f"\n✅ Total {len(all_results)} artikel dari {len(keywords)} keywords")


def main():
    """
    Menu utama untuk memilih contoh
    """
    print("\n" + "="*80)
    print("📚 CONTOH PENGGUNAAN TRIBUNNEWS SCRAPER")
    print("="*80)
    print("\nPilih contoh yang ingin dijalankan:")
    print("1. Scraping Dasar")
    print("2. Multiple Keywords")
    print("3. Scraping dengan Filter")
    print("4. Mengakses Hasil Scraping")
    print("5. Error Handling")
    print("6. Custom Filename")
    print("7. Batch Scraping")
    print("8. Jalankan Semua Contoh")
    print("0. Keluar")
    
    choice = input("\nPilihan [1-8, 0]: ").strip()
    
    examples = {
        '1': example_1_basic_scraping,
        '2': example_2_multiple_keywords,
        '3': example_3_filtered_scraping,
        '4': example_4_accessing_results,
        '5': example_5_error_handling,
        '6': example_6_custom_filename,
        '7': example_7_batch_scraping
    }
    
    if choice == '0':
        print("\n👋 Terima kasih!")
        return
    elif choice == '8':
        for func in examples.values():
            func()
            time.sleep(3)
    elif choice in examples:
        examples[choice]()
    else:
        print("❌ Pilihan tidak valid!")


if __name__ == "__main__":
    main()
