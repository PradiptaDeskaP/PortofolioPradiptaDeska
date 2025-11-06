"""
Radar Surabaya News Scraper
============================
Professional web scraper untuk mengambil artikel berita dari Radar Surabaya
Dibuat oleh: Data Engineer & AI Engineer dengan 45 tahun pengalaman

Features:
- Search berita berdasarkan keyword
- Scraping judul, tanggal, kategori dari halaman hasil pencarian
- Scraping detail artikel (penulis dan konten lengkap)
- Export hasil ke CSV dan JSON
- Error handling dan logging yang komprehensif
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime
from urllib.parse import quote_plus, urljoin
import time
import re
from typing import List, Dict, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('radar_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RadarSurabayaScraper:
    """
    Web scraper untuk Radar Surabaya dengan kemampuan:
    - Search otomatis
    - Scraping multi-page
    - Data extraction yang robust
    """
    
    def __init__(self):
        self.base_url = "https://radarsurabaya.jawapos.com"
        self.search_url = f"{self.base_url}/search"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.results = []
        
    def search_news(self, keyword: str, max_pages: int = 5) -> List[Dict]:
        """
        Melakukan pencarian berita berdasarkan keyword
        
        Args:
            keyword: Kata kunci pencarian (contoh: "harga jagung")
            max_pages: Maksimum halaman yang akan di-scrape
            
        Returns:
            List of dictionaries berisi data berita
        """
        logger.info(f"Memulai pencarian berita dengan keyword: '{keyword}'")
        self.results = []
        
        # Format keyword untuk URL
        encoded_keyword = quote_plus(keyword)
        search_query_url = f"{self.search_url}?q={encoded_keyword}"
        
        page = 1
        while page <= max_pages:
            try:
                # Tambahkan parameter page jika bukan halaman pertama
                if page > 1:
                    current_url = f"{search_query_url}&page={page}"
                else:
                    current_url = search_query_url
                    
                logger.info(f"Scraping halaman {page}: {current_url}")
                
                response = self.session.get(current_url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Cari artikel di halaman pencarian
                articles = self._extract_search_results(soup)
                
                if not articles:
                    logger.info(f"Tidak ada artikel ditemukan di halaman {page}. Menghentikan pencarian.")
                    break
                
                logger.info(f"Ditemukan {len(articles)} artikel di halaman {page}")
                
                # Scrape detail untuk setiap artikel
                for idx, article in enumerate(articles, 1):
                    logger.info(f"Mengambil detail artikel {idx}/{len(articles)}: {article.get('title', 'Unknown')[:50]}...")
                    detail = self._scrape_article_detail(article['url'])
                    
                    if detail:
                        article.update(detail)
                        self.results.append(article)
                    
                    # Delay untuk menghindari rate limiting
                    time.sleep(1)
                
                page += 1
                time.sleep(2)  # Delay antar halaman
                
            except requests.RequestException as e:
                logger.error(f"Error saat mengakses halaman {page}: {e}")
                break
            except Exception as e:
                logger.error(f"Error tidak terduga pada halaman {page}: {e}")
                break
        
        logger.info(f"Selesai! Total {len(self.results)} artikel berhasil di-scrape")
        return self.results
    
    def _extract_search_results(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract artikel dari halaman hasil pencarian
        
        Args:
            soup: BeautifulSoup object dari halaman pencarian
            
        Returns:
            List of dictionaries dengan informasi dasar artikel
        """
        articles = []
        
        # Cari container artikel dengan berbagai selector
        # Selector utama
        article_containers = soup.select('div.latest__wrap > div')
        
        # Jika tidak ditemukan, coba selector alternatif
        if not article_containers:
            article_containers = soup.select('article.latest')
        
        if not article_containers:
            article_containers = soup.select('div.latest')
        
        for container in article_containers:
            try:
                article_data = {}
                
                # Extract judul dan URL
                title_elem = container.select_one('h2 > a')
                if not title_elem:
                    title_elem = container.select_one('h2 a')
                if not title_elem:
                    title_elem = container.select_one('.latest__right h2 a')
                    
                if title_elem:
                    article_data['title'] = title_elem.get_text(strip=True)
                    article_data['url'] = urljoin(self.base_url, title_elem.get('href', ''))
                else:
                    continue  # Skip jika tidak ada judul
                
                # Extract tanggal
                date_elem = container.select_one('date')
                if not date_elem:
                    date_elem = container.select_one('time')
                if not date_elem:
                    date_elem = container.select_one('.latest__right date')
                    
                if date_elem:
                    article_data['date'] = date_elem.get_text(strip=True)
                else:
                    article_data['date'] = 'Unknown'
                
                # Extract kategori
                category_elem = container.select_one('h4 > a')
                if not category_elem:
                    category_elem = container.select_one('h4 a')
                if not category_elem:
                    category_elem = container.select_one('.latest__right h4 a')
                    
                if category_elem:
                    article_data['category'] = category_elem.get_text(strip=True)
                else:
                    article_data['category'] = 'Unknown'
                
                # Extract excerpt jika ada
                excerpt_elem = container.select_one('p')
                if excerpt_elem:
                    article_data['excerpt'] = excerpt_elem.get_text(strip=True)
                else:
                    article_data['excerpt'] = ''
                
                articles.append(article_data)
                
            except Exception as e:
                logger.warning(f"Error saat extract artikel dari container: {e}")
                continue
        
        return articles
    
    def _scrape_article_detail(self, url: str) -> Optional[Dict]:
        """
        Scrape detail artikel dari halaman artikel
        
        Args:
            url: URL artikel lengkap
            
        Returns:
            Dictionary berisi author dan content, atau None jika gagal
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            detail_data = {}
            
            # Extract author
            author_elem = soup.select_one('div.read__info__author > a')
            if not author_elem:
                author_elem = soup.select_one('div.read__info__author a')
            if not author_elem:
                author_elem = soup.select_one('.read__info__author a')
            if not author_elem:
                author_elem = soup.select_one('a[rel="author"]')
            if not author_elem:
                # Coba cari dari meta tag
                author_meta = soup.select_one('meta[name="author"]')
                if author_meta:
                    detail_data['author'] = author_meta.get('content', 'Unknown')
                else:
                    detail_data['author'] = 'Unknown'
            else:
                detail_data['author'] = author_elem.get_text(strip=True)
            
            # Extract content
            # Coba beberapa selector untuk konten
            content_elem = soup.select_one('div.col-bs10-7 > div')
            if not content_elem:
                content_elem = soup.select_one('div.read__content')
            if not content_elem:
                content_elem = soup.select_one('article div[itemprop="articleBody"]')
            if not content_elem:
                content_elem = soup.select_one('.entry-content')
            
            if content_elem:
                # Hapus script, style, dan elemen yang tidak diinginkan
                for unwanted in content_elem.select('script, style, iframe, .ads, .advertisement'):
                    unwanted.decompose()
                
                # Ambil semua paragraf
                paragraphs = content_elem.find_all(['p', 'div'], recursive=True)
                content_text = []
                
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:  # Filter paragraf yang terlalu pendek
                        content_text.append(text)
                
                detail_data['content'] = '\n\n'.join(content_text)
                
                # Jika konten masih kosong, ambil semua text
                if not detail_data['content']:
                    detail_data['content'] = content_elem.get_text(separator='\n', strip=True)
            else:
                detail_data['content'] = 'Content not found'
            
            # Extract tanggal publikasi yang lebih detail jika ada
            pub_date_elem = soup.select_one('time[datetime]')
            if pub_date_elem:
                detail_data['published_datetime'] = pub_date_elem.get('datetime', '')
            
            return detail_data
            
        except requests.RequestException as e:
            logger.error(f"Error saat mengakses detail artikel {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error tidak terduga saat scrape detail {url}: {e}")
            return None
    
    def save_to_csv(self, filename: str = None):
        """
        Simpan hasil scraping ke file CSV
        
        Args:
            filename: Nama file output (default: radar_surabaya_YYYYMMDD_HHMMSS.csv)
        """
        if not self.results:
            logger.warning("Tidak ada data untuk disimpan")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"radar_surabaya_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['title', 'url', 'date', 'category', 'author', 'excerpt', 'content', 'published_datetime']
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                
                writer.writeheader()
                writer.writerows(self.results)
            
            logger.info(f"Data berhasil disimpan ke {filename}")
            print(f"\n✓ Data berhasil disimpan ke: {filename}")
            
        except Exception as e:
            logger.error(f"Error saat menyimpan ke CSV: {e}")
    
    def save_to_json(self, filename: str = None):
        """
        Simpan hasil scraping ke file JSON
        
        Args:
            filename: Nama file output (default: radar_surabaya_YYYYMMDD_HHMMSS.json)
        """
        if not self.results:
            logger.warning("Tidak ada data untuk disimpan")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"radar_surabaya_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Data berhasil disimpan ke {filename}")
            print(f"✓ Data berhasil disimpan ke: {filename}")
            
        except Exception as e:
            logger.error(f"Error saat menyimpan ke JSON: {e}")
    
    def print_summary(self):
        """
        Cetak ringkasan hasil scraping
        """
        if not self.results:
            print("\nTidak ada data untuk ditampilkan")
            return
        
        print("\n" + "="*80)
        print(f"RINGKASAN HASIL SCRAPING - Total: {len(self.results)} artikel")
        print("="*80)
        
        for idx, article in enumerate(self.results, 1):
            print(f"\n[{idx}] {article.get('title', 'Unknown')}")
            print(f"    URL: {article.get('url', 'Unknown')}")
            print(f"    Tanggal: {article.get('date', 'Unknown')}")
            print(f"    Kategori: {article.get('category', 'Unknown')}")
            print(f"    Penulis: {article.get('author', 'Unknown')}")
            print(f"    Konten: {article.get('content', '')[:100]}..." if article.get('content') else "    Konten: N/A")
        
        print("\n" + "="*80)


def main():
    """
    Fungsi utama untuk menjalankan scraper
    """
    print("="*80)
    print("RADAR SURABAYA NEWS SCRAPER")
    print("Scraper profesional untuk artikel berita Radar Surabaya")
    print("="*80)
    
    # Inisialisasi scraper
    scraper = RadarSurabayaScraper()
    
    # Minta input dari user
    print("\nMasukkan keyword berita yang ingin Anda cari:")
    print("Contoh: harga jagung, pemilu, pendidikan, kesehatan, dll.")
    keyword = input("Keyword: ").strip()
    
    if not keyword:
        print("Error: Keyword tidak boleh kosong!")
        return
    
    # Tanya jumlah halaman
    try:
        max_pages_input = input("\nBerapa halaman yang ingin di-scrape? (default: 5): ").strip()
        max_pages = int(max_pages_input) if max_pages_input else 5
        max_pages = max(1, min(max_pages, 20))  # Batasi antara 1-20 halaman
    except ValueError:
        max_pages = 5
        print("Input tidak valid, menggunakan default: 5 halaman")
    
    print(f"\n🚀 Memulai scraping untuk keyword: '{keyword}' (maksimal {max_pages} halaman)")
    print("Mohon tunggu, proses ini mungkin memakan waktu beberapa menit...\n")
    
    # Lakukan scraping
    results = scraper.search_news(keyword, max_pages=max_pages)
    
    if not results:
        print("\n❌ Tidak ada artikel ditemukan untuk keyword tersebut.")
        print("Coba dengan keyword lain atau periksa koneksi internet Anda.")
        return
    
    # Tampilkan ringkasan
    scraper.print_summary()
    
    # Simpan hasil
    print("\n" + "="*80)
    print("MENYIMPAN HASIL")
    print("="*80)
    
    # Tanya format output
    print("\nPilih format output:")
    print("1. CSV")
    print("2. JSON")
    print("3. Keduanya")
    
    choice = input("Pilihan (1/2/3, default: 3): ").strip()
    
    if choice in ['1', '']:
        scraper.save_to_csv()
    elif choice == '2':
        scraper.save_to_json()
    else:  # Default atau 3
        scraper.save_to_csv()
        scraper.save_to_json()
    
    print("\n" + "="*80)
    print("✓ SCRAPING SELESAI!")
    print(f"✓ Total artikel berhasil di-scrape: {len(results)}")
    print("✓ Log tersimpan di: radar_scraper.log")
    print("="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping dibatalkan oleh user")
        logger.info("Scraping dibatalkan oleh user")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        logger.error(f"Error fatal: {e}", exc_info=True)
