"""
Example Usage Script - Radar Surabaya Scraper
==============================================
Contoh penggunaan scraper secara programmatic

Berbagai contoh use case untuk referensi Anda
"""

from radar_surabaya_scraper import RadarSurabayaScraper
import time

def example_1_basic_usage():
    """
    Example 1: Basic usage - scrape berita dengan keyword tertentu
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    scraper = RadarSurabayaScraper()
    
    # Scrape 3 halaman berita tentang "harga jagung"
    results = scraper.search_news("harga jagung", max_pages=3)
    
    # Print hasil
    print(f"\nBerhasil scrape {len(results)} artikel")
    
    # Save to files
    scraper.save_to_csv("contoh_harga_jagung.csv")
    scraper.save_to_json("contoh_harga_jagung.json")


def example_2_multiple_keywords():
    """
    Example 2: Scrape multiple keywords
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Multiple Keywords")
    print("="*80)
    
    keywords = ["pendidikan", "kesehatan", "ekonomi"]
    
    for keyword in keywords:
        print(f"\n--- Scraping keyword: {keyword} ---")
        
        scraper = RadarSurabayaScraper()
        results = scraper.search_news(keyword, max_pages=2)
        
        # Save with keyword-specific filename
        scraper.save_to_csv(f"hasil_{keyword}.csv")
        
        print(f"✓ Selesai: {len(results)} artikel untuk '{keyword}'")
        
        # Delay antar keyword untuk menghindari rate limiting
        time.sleep(5)


def example_3_filter_by_date():
    """
    Example 3: Filter hasil berdasarkan tanggal
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Filter by Date")
    print("="*80)
    
    scraper = RadarSurabayaScraper()
    results = scraper.search_news("surabaya", max_pages=3)
    
    # Filter hanya artikel hari ini (contoh sederhana)
    today_articles = []
    for article in results:
        date_str = article.get('date', '').lower()
        if 'hari ini' in date_str or 'jam' in date_str or 'menit' in date_str:
            today_articles.append(article)
    
    print(f"\nTotal artikel: {len(results)}")
    print(f"Artikel hari ini: {len(today_articles)}")
    
    # Simpan hanya artikel hari ini
    scraper.results = today_articles
    scraper.save_to_csv("artikel_hari_ini.csv")


def example_4_filter_by_category():
    """
    Example 4: Filter hasil berdasarkan kategori
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Filter by Category")
    print("="*80)
    
    scraper = RadarSurabayaScraper()
    results = scraper.search_news("berita terkini", max_pages=5)
    
    # Group by category
    categories = {}
    for article in results:
        category = article.get('category', 'Unknown')
        if category not in categories:
            categories[category] = []
        categories[category].append(article)
    
    # Print summary
    print("\nRingkasan per kategori:")
    for category, articles in categories.items():
        print(f"  - {category}: {len(articles)} artikel")
    
    # Save per category
    for category, articles in categories.items():
        scraper.results = articles
        safe_filename = category.replace('/', '_').replace(' ', '_')
        scraper.save_to_csv(f"kategori_{safe_filename}.csv")


def example_5_extract_statistics():
    """
    Example 5: Extract statistik dari hasil scraping
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Extract Statistics")
    print("="*80)
    
    scraper = RadarSurabayaScraper()
    results = scraper.search_news("ekonomi", max_pages=3)
    
    # Hitung statistik
    total_articles = len(results)
    total_words = sum(len(article.get('content', '').split()) for article in results)
    avg_words = total_words / total_articles if total_articles > 0 else 0
    
    authors = set(article.get('author', 'Unknown') for article in results)
    categories = set(article.get('category', 'Unknown') for article in results)
    
    print(f"\n📊 Statistik Scraping:")
    print(f"  Total Artikel: {total_articles}")
    print(f"  Total Kata: {total_words:,}")
    print(f"  Rata-rata Kata per Artikel: {avg_words:.0f}")
    print(f"  Jumlah Penulis Unik: {len(authors)}")
    print(f"  Jumlah Kategori: {len(categories)}")
    print(f"\n  Penulis: {', '.join(list(authors)[:5])}")
    print(f"  Kategori: {', '.join(list(categories))}")


def example_6_search_in_content():
    """
    Example 6: Search specific keywords dalam content
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: Search in Content")
    print("="*80)
    
    scraper = RadarSurabayaScraper()
    results = scraper.search_news("harga pangan", max_pages=3)
    
    # Cari artikel yang mengandung kata kunci spesifik
    search_terms = ["jagung", "beras", "minyak goreng"]
    
    for term in search_terms:
        matching_articles = []
        for article in results:
            content = article.get('content', '').lower()
            title = article.get('title', '').lower()
            if term.lower() in content or term.lower() in title:
                matching_articles.append(article)
        
        print(f"\n'{term}': {len(matching_articles)} artikel")
        
        if matching_articles:
            scraper.results = matching_articles
            scraper.save_to_csv(f"artikel_tentang_{term}.csv")


def example_7_custom_processing():
    """
    Example 7: Custom processing pada hasil
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Custom Processing")
    print("="*80)
    
    scraper = RadarSurabayaScraper()
    results = scraper.search_news("teknologi", max_pages=2)
    
    # Tambah field custom
    for article in results:
        # Hitung panjang konten
        article['content_length'] = len(article.get('content', ''))
        article['word_count'] = len(article.get('content', '').split())
        
        # Kategorikan berdasarkan panjang
        if article['word_count'] < 200:
            article['length_category'] = 'short'
        elif article['word_count'] < 500:
            article['length_category'] = 'medium'
        else:
            article['length_category'] = 'long'
        
        # Extract keywords sederhana (5 kata terpanjang)
        words = article.get('content', '').split()
        long_words = sorted([w for w in words if len(w) > 5], key=len, reverse=True)[:5]
        article['keywords'] = ', '.join(long_words)
    
    scraper.results = results
    scraper.save_to_json("artikel_with_analysis.json")
    
    print(f"\n✓ Processed {len(results)} artikel dengan analisis tambahan")


def main():
    """
    Main function - pilih example yang ingin dijalankan
    """
    print("="*80)
    print("RADAR SURABAYA SCRAPER - EXAMPLE USAGE")
    print("="*80)
    
    print("\nPilih example yang ingin dijalankan:")
    print("1. Basic Usage")
    print("2. Multiple Keywords")
    print("3. Filter by Date")
    print("4. Filter by Category")
    print("5. Extract Statistics")
    print("6. Search in Content")
    print("7. Custom Processing")
    print("8. Run All Examples")
    print("0. Exit")
    
    choice = input("\nPilihan (0-8): ").strip()
    
    examples = {
        '1': example_1_basic_usage,
        '2': example_2_multiple_keywords,
        '3': example_3_filter_by_date,
        '4': example_4_filter_by_category,
        '5': example_5_extract_statistics,
        '6': example_6_search_in_content,
        '7': example_7_custom_processing,
    }
    
    if choice == '8':
        # Run all examples
        for func in examples.values():
            try:
                func()
                time.sleep(3)
            except Exception as e:
                print(f"Error in example: {e}")
    elif choice in examples:
        examples[choice]()
    elif choice == '0':
        print("Goodbye!")
        return
    else:
        print("Pilihan tidak valid!")
        return
    
    print("\n" + "="*80)
    print("✓ Example selesai dijalankan!")
    print("="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Example dibatalkan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
