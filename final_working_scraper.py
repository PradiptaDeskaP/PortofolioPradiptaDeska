#!/usr/bin/env python3
"""
Final Working Radar Surabaya News Scraper
Menggunakan teknik anti-detection yang canggih
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, quote
import re
import logging
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalWorkingRadarScraper:
    def __init__(self):
        self.base_url = "https://radarsurabaya.jawapos.com/"
        self.session = self.setup_session()
    
    def setup_session(self):
        """Setup session dengan anti-detection"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Headers yang sangat realistis
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-GPC': '1'
        })
        
        return session
    
    def random_delay(self, min_seconds=2, max_seconds=5):
        """Random delay untuk menghindari deteksi"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def get_page_content(self, url, retries=3):
        """Mengambil konten halaman dengan retry dan anti-detection"""
        for attempt in range(retries):
            try:
                logger.info(f"Fetching (attempt {attempt + 1}): {url}")
                
                # Random delay
                self.random_delay()
                
                # Simulasi referer
                if 'search' in url or 'cari' in url:
                    self.session.headers.update({'Referer': self.base_url})
                
                response = self.session.get(url, timeout=30, allow_redirects=True)
                
                # Cek status code
                if response.status_code == 403:
                    logger.warning(f"403 Forbidden - mungkin diblokir")
                    if attempt < retries - 1:
                        self.random_delay(5, 10)
                        continue
                
                response.raise_for_status()
                logger.info(f"Successfully fetched: {url}")
                return response.text
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    self.random_delay(3, 8)
                else:
                    logger.error(f"All attempts failed for {url}")
                    return None
        
        return None
    
    def search_news(self, search_query):
        """Mencari berita dengan berbagai metode"""
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
                if content and len(content) > 1000:  # Pastikan konten cukup panjang
                    soup = BeautifulSoup(content, 'html.parser')
                    articles = self.extract_articles_from_soup(soup)
                    if articles:
                        logger.info(f"Berhasil menemukan {len(articles)} artikel")
                        return articles
                    else:
                        logger.warning(f"Tidak ada artikel ditemukan di {search_url}")
            
            # Jika pencarian gagal, coba ambil dari halaman utama
            logger.info("Mencoba mengambil berita terbaru dari halaman utama...")
            content = self.get_page_content(self.base_url)
            if content and len(content) > 1000:
                soup = BeautifulSoup(content, 'html.parser')
                articles = self.extract_articles_from_soup(soup)
                if articles:
                    logger.info(f"Berhasil menemukan {len(articles)} artikel dari halaman utama")
                    return articles
            
            return []
            
        except Exception as e:
            logger.error(f"Error dalam pencarian: {e}")
            return []
    
    def extract_articles_from_soup(self, soup):
        """Ekstrak artikel dari BeautifulSoup object"""
        articles = []
        
        try:
            # Cari semua link yang mengarah ke artikel
            article_links = soup.find_all('a', href=re.compile(r'radarsurabaya\.jawapos\.com.*/\d{4}/'))
            
            # Juga cari dengan pattern lain
            additional_links = soup.find_all('a', href=re.compile(r'radarsurabaya\.jawapos\.com.*berita'))
            article_links.extend(additional_links)
            
            # Cari dengan class atau id yang umum
            class_links = soup.find_all('a', class_=re.compile(r'article|news|post|item', re.I))
            for link in class_links:
                if link.get('href') and 'radarsurabaya.jawapos.com' in link.get('href', ''):
                    article_links.append(link)
            
            # Cari semua link yang mengandung kata kunci
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                if ('radarsurabaya.jawapos.com' in href and 
                    any(word in href.lower() for word in ['berita', 'news', 'artikel', 'article']) and
                    '/tag/' not in href and '/category/' not in href):
                    article_links.append(link)
            
            logger.info(f"Ditemukan {len(article_links)} link artikel potensial")
            
            # Remove duplicates
            seen_urls = set()
            unique_links = []
            for link in article_links:
                url = link.get('href')
                if url and url not in seen_urls:
                    if not url.startswith('http'):
                        url = urljoin(self.base_url, url)
                    seen_urls.add(url)
                    unique_links.append((link, url))
            
            # Proses setiap link
            for i, (link, article_url) in enumerate(unique_links[:15]):  # Batasi 15 artikel
                try:
                    # Cari judul
                    title = link.get_text(strip=True)
                    if not title:
                        # Coba cari di parent element
                        parent = link.parent
                        if parent:
                            title = parent.get_text(strip=True)
                    
                    if title and len(title) > 10 and len(title) < 200:
                        article = {
                            'title': title,
                            'link': article_url,
                            'date': 'N/A',
                            'category': 'N/A',
                            'author': 'N/A',
                            'content': 'N/A'
                        }
                        articles.append(article)
                        logger.info(f"Artikel {i+1}: {title[:50]}...")
                
                except Exception as e:
                    logger.debug(f"Error processing article {i+1}: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Error extracting articles from soup: {e}")
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
                'a[class*="author"]', 'p[class*="author"]'
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
                '.single-content', '.post-body', '.article-body'
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Hapus script dan style tags
                    for script in content_elem(["script", "style", "nav", "header", "footer"]):
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
                
                # Delay untuk menghindari rate limiting
                self.random_delay(3, 6)
            
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
    scraper = FinalWorkingRadarScraper()
    
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
            print("\nKemungkinan penyebab:")
            print("1. Website memblokir akses scraping")
            print("2. Perlu menggunakan proxy atau VPN")
            print("3. Website menggunakan JavaScript yang kompleks")
            print("4. Perlu menunggu beberapa saat sebelum mencoba lagi")
    
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh user.")
    except Exception as e:
        print(f"Terjadi error: {e}")

if __name__ == "__main__":
    main()