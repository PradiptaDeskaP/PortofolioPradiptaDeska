#!/usr/bin/env python3
"""
Simple Working Radar Surabaya News Scraper
Versi sederhana yang dapat bekerja dengan baik
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, quote
import re
import logging
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleWorkingRadarSurabayaScraper:
    def __init__(self):
        self.base_url = "https://radarsurabaya.jawapos.com/"
        self.session = requests.Session()
        
        # Setup session dengan headers yang lebih realistis
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/',
        })
    
    def get_page_content(self, url, retries=3):
        """Mengambil konten halaman dengan retry mechanism"""
        for attempt in range(retries):
            try:
                logger.info(f"Fetching (attempt {attempt + 1}): {url}")
                
                # Random delay untuk menghindari deteksi
                time.sleep(random.uniform(2, 5))
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                logger.info(f"Successfully fetched: {url}")
                return response.text
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(3, 6))
                else:
                    logger.error(f"All attempts failed for {url}")
                    return None
        
        return None
    
    def search_news(self, search_query):
        """Mencari berita berdasarkan query"""
        try:
            logger.info(f"Memulai pencarian untuk: {search_query}")
            
            # Coba berbagai URL pencarian
            search_urls = [
                f"https://radarsurabaya.jawapos.com/?s={quote(search_query)}",
                f"https://radarsurabaya.jawapos.com/search/?q={quote(search_query)}",
                f"https://radarsurabaya.jawapos.com/cari/?search={quote(search_query)}",
                f"https://radarsurabaya.jawapos.com/berita/?search={quote(search_query)}",
                f"https://radarsurabaya.jawapos.com/?search={quote(search_query)}"
            ]
            
            for search_url in search_urls:
                logger.info(f"Mencoba URL: {search_url}")
                content = self.get_page_content(search_url)
                if content:
                    soup = BeautifulSoup(content, 'html.parser')
                    articles = self.extract_articles(soup)
                    if articles:
                        logger.info(f"Berhasil menemukan {len(articles)} artikel")
                        return articles
                    else:
                        logger.warning(f"Tidak ada artikel ditemukan di {search_url}")
            
            # Jika pencarian gagal, coba ambil dari halaman utama
            logger.info("Mencoba mengambil berita terbaru dari halaman utama...")
            content = self.get_page_content(self.base_url)
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                articles = self.extract_articles(soup)
                if articles:
                    logger.info(f"Berhasil menemukan {len(articles)} artikel dari halaman utama")
                    return articles
            
            return []
            
        except Exception as e:
            logger.error(f"Error dalam pencarian: {e}")
            return []
    
    def extract_articles(self, soup):
        """Ekstrak artikel dari halaman"""
        articles = []
        
        try:
            # Cari semua link yang mengarah ke artikel
            # Gunakan regex yang lebih spesifik untuk artikel
            article_patterns = [
                r'radarsurabaya\.jawapos\.com.*/\d{4}/\d{2}/\d{2}/',  # Format tanggal
                r'radarsurabaya\.jawapos\.com.*/\d{4}/\d{2}/',       # Format bulan
                r'radarsurabaya\.jawapos\.com.*/berita/',             # Path berita
                r'radarsurabaya\.jawapos\.com.*/news/'                # Path news
            ]
            
            all_links = soup.find_all('a', href=True)
            article_links = []
            
            for link in all_links:
                href = link.get('href', '')
                for pattern in article_patterns:
                    if re.search(pattern, href):
                        article_links.append(link)
                        break
            
            logger.info(f"Ditemukan {len(article_links)} link artikel potensial")
            
            # Proses setiap link
            for i, link in enumerate(article_links[:15]):  # Batasi 15 artikel
                try:
                    article_url = link.get('href')
                    if not article_url.startswith('http'):
                        article_url = urljoin(self.base_url, article_url)
                    
                    # Cari judul
                    title = link.get_text(strip=True)
                    if not title:
                        # Coba cari di parent element
                        parent = link.parent
                        if parent:
                            title = parent.get_text(strip=True)
                    
                    # Cari tanggal dan kategori dari parent elements
                    date = "N/A"
                    category = "N/A"
                    
                    # Cari tanggal
                    date_elem = link.find_parent().find(['date', 'time', 'span', 'div'], 
                                                      class_=re.compile(r'date|time|published', re.I))
                    if date_elem:
                        date = date_elem.get_text(strip=True)
                    
                    # Cari kategori
                    cat_elem = link.find_parent().find(['span', 'div', 'a'], 
                                                     class_=re.compile(r'category|cat|tag', re.I))
                    if cat_elem:
                        category = cat_elem.get_text(strip=True)
                    
                    if title and len(title) > 10:  # Pastikan judul tidak kosong
                        article = {
                            'title': title,
                            'link': article_url,
                            'date': date,
                            'category': category,
                            'author': 'N/A',
                            'content': 'N/A'
                        }
                        articles.append(article)
                        logger.info(f"Artikel {len(articles)}: {title[:50]}...")
                
                except Exception as e:
                    logger.debug(f"Error processing article link {i+1}: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Error extracting articles: {e}")
            return []
    
    def scrape_article_detail(self, article_url):
        """Scraping detail artikel"""
        try:
            logger.info(f"Scraping detail: {article_url}")
            
            content = self.get_page_content(article_url)
            if not content:
                return {'author': 'N/A', 'content': 'N/A'}
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Cari penulis
            author = "N/A"
            author_selectors = [
                '.author', '.writer', '.byline', '.post-author',
                '.article-author', '.meta .author', '.meta .writer',
                'span[class*="author"]', 'div[class*="author"]',
                'a[class*="author"]', 'p[class*="author"]',
                '.entry-meta .author', '.post-meta .author'
            ]
            
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    author_text = author_elem.get_text(strip=True)
                    if author_text and len(author_text) < 100:
                        author = author_text
                        break
            
            # Cari konten artikel
            content_text = "N/A"
            content_selectors = [
                'article', '.content', '.article-content', '.post-content',
                '.entry-content', '.news-content', '.main-content', '.story-content',
                '.single-content', '.post-body', '.article-body', '.story-body',
                '.entry-body', '.post-text', '.article-text'
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Hapus script dan style tags
                    for script in content_elem(["script", "style", "nav", "header", "footer", "aside"]):
                        script.decompose()
                    
                    content_text = content_elem.get_text(strip=True)
                    if content_text and len(content_text) > 100:
                        break
            
            return {
                'author': author,
                'content': content_text
            }
            
        except Exception as e:
            logger.error(f"Error scraping article detail: {e}")
            return {'author': 'N/A', 'content': 'N/A'}
    
    def scrape_news_complete(self, search_query, max_articles=5):
        """Fungsi utama untuk scraping berita lengkap"""
        try:
            logger.info(f"Memulai scraping berita untuk query: {search_query}")
            
            # Cari berita
            news_list = self.search_news(search_query)
            
            if not news_list:
                logger.warning("Tidak ada berita ditemukan")
                return []
            
            # Batasi jumlah artikel
            limited_news = news_list[:max_articles]
            
            # Scraping detail setiap artikel
            complete_news = []
            for i, news in enumerate(limited_news):
                logger.info(f"Memproses artikel {i+1}/{len(limited_news)}")
                
                if news['link'] != "N/A":
                    article_detail = self.scrape_article_detail(news['link'])
                    news.update(article_detail)
                else:
                    news.update({'author': 'N/A', 'content': 'N/A'})
                
                complete_news.append(news)
                
                # Random delay untuk menghindari rate limiting
                time.sleep(random.uniform(3, 6))
            
            logger.info(f"Scraping selesai. Total {len(complete_news)} artikel berhasil diambil")
            return complete_news
            
        except Exception as e:
            logger.error(f"Error dalam proses scraping: {e}")
            return []
    
    def save_to_json(self, data, filename):
        """Simpan data ke file JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data berhasil disimpan ke {filename}")
        except Exception as e:
            logger.error(f"Error saat menyimpan data: {e}")

def main():
    """Fungsi utama"""
    scraper = SimpleWorkingRadarSurabayaScraper()
    
    try:
        # Input query pencarian
        search_query = input("Masukkan kata kunci pencarian berita: ")
        
        if not search_query.strip():
            print("Query pencarian tidak boleh kosong!")
            return
        
        # Lakukan scraping
        print(f"\nMemulai scraping berita untuk: '{search_query}'")
        print("Mohon tunggu...")
        
        news_data = scraper.scrape_news_complete(search_query, max_articles=5)
        
        if news_data:
            # Tampilkan hasil
            print(f"\n=== HASIL SCRAPING BERITA ===")
            print(f"Total artikel ditemukan: {len(news_data)}")
            print("=" * 50)
            
            for i, news in enumerate(news_data, 1):
                print(f"\n{i}. JUDUL: {news['title']}")
                print(f"   TANGGAL: {news['date']}")
                print(f"   KATEGORI: {news['category']}")
                print(f"   PENULIS: {news['author']}")
                print(f"   LINK: {news['link']}")
                print(f"   KONTEN: {news['content'][:200]}...")
                print("-" * 50)
            
            # Simpan ke file JSON
            filename = f"berita_radar_surabaya_{search_query.replace(' ', '_')}.json"
            scraper.save_to_json(news_data, filename)
            print(f"\nData berhasil disimpan ke file: {filename}")
            
        else:
            print("Tidak ada berita ditemukan atau terjadi error saat scraping.")
    
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh user.")
    except Exception as e:
        print(f"Terjadi error: {e}")

if __name__ == "__main__":
    main()