import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, quote, urlparse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException
import logging
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RadarSurabayaScraper:
    def __init__(self):
        self.base_url = "https://radarsurabaya.jawapos.com/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver dengan konfigurasi optimal"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Chrome driver berhasil diinisialisasi")
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {e}")
            raise
    
    def get_page_content(self, url):
        """Mengambil konten halaman menggunakan requests"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching page content: {e}")
            return None
    
    def search_news_requests(self, search_query):
        """Mencari berita menggunakan requests dan BeautifulSoup"""
        try:
            logger.info(f"Memulai pencarian menggunakan requests untuk: {search_query}")
            
            # Coba berbagai URL pencarian yang mungkin
            search_urls = [
                f"https://radarsurabaya.jawapos.com/?s={quote(search_query)}",
                f"https://radarsurabaya.jawapos.com/search/?q={quote(search_query)}",
                f"https://radarsurabaya.jawapos.com/cari/?search={quote(search_query)}",
                f"https://radarsurabaya.jawapos.com/berita/?search={quote(search_query)}"
            ]
            
            for search_url in search_urls:
                logger.info(f"Mencoba URL: {search_url}")
                content = self.get_page_content(search_url)
                if content:
                    soup = BeautifulSoup(content, 'html.parser')
                    articles = self.extract_articles_from_soup(soup)
                    if articles:
                        logger.info(f"Berhasil menemukan {len(articles)} artikel dari {search_url}")
                        return articles
                    else:
                        logger.warning(f"Tidak ada artikel ditemukan di {search_url}")
            
            return []
            
        except Exception as e:
            logger.error(f"Error dalam pencarian menggunakan requests: {e}")
            return []
    
    def extract_articles_from_soup(self, soup):
        """Ekstrak artikel dari BeautifulSoup object"""
        articles = []
        
        try:
            # Cari berbagai kemungkinan container artikel
            article_containers = [
                soup.find_all('div', class_=re.compile(r'article|news|post|item', re.I)),
                soup.find_all('article'),
                soup.find_all('div', class_=re.compile(r'content|main', re.I)),
                soup.find_all('div', class_=re.compile(r'list|grid', re.I))
            ]
            
            # Flatten list dan remove duplicates
            all_containers = []
            for container_list in article_containers:
                all_containers.extend(container_list)
            
            # Remove duplicates
            seen = set()
            unique_containers = []
            for container in all_containers:
                if container not in seen:
                    seen.add(container)
                    unique_containers.append(container)
            
            logger.info(f"Ditemukan {len(unique_containers)} container potensial")
            
            for container in unique_containers:
                try:
                    article = self.extract_single_article(container)
                    if article and article.get('title') and article['title'] != "N/A":
                        articles.append(article)
                        logger.info(f"Artikel berhasil diekstrak: {article['title'][:50]}...")
                except Exception as e:
                    logger.debug(f"Error extracting article: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Error extracting articles from soup: {e}")
            return []
    
    def extract_single_article(self, container):
        """Ekstrak data dari single article container"""
        article = {
            'title': 'N/A',
            'link': 'N/A',
            'date': 'N/A',
            'category': 'N/A',
            'author': 'N/A',
            'content': 'N/A'
        }
        
        try:
            # Cari judul dan link
            title_selectors = [
                'h1 a', 'h2 a', 'h3 a', 'h4 a',
                '.title a', '.headline a', '.post-title a',
                'a[href*="radarsurabaya"]'
            ]
            
            for selector in title_selectors:
                title_elem = container.select_one(selector)
                if title_elem:
                    article['title'] = title_elem.get_text(strip=True)
                    article['link'] = urljoin(self.base_url, title_elem.get('href', ''))
                    break
            
            # Cari tanggal
            date_selectors = [
                'date', 'time', '.date', '.time', '.published',
                '.post-date', '.article-date', '.news-date'
            ]
            
            for selector in date_selectors:
                date_elem = container.select_one(selector)
                if date_elem:
                    article['date'] = date_elem.get_text(strip=True)
                    break
            
            # Cari kategori
            category_selectors = [
                '.category a', '.cat a', '.tag a', '.label a',
                'h4 a', '.meta a', '.breadcrumb a'
            ]
            
            for selector in category_selectors:
                cat_elem = container.select_one(selector)
                if cat_elem:
                    article['category'] = cat_elem.get_text(strip=True)
                    break
            
            return article
            
        except Exception as e:
            logger.debug(f"Error extracting single article: {e}")
            return article
    
    def scrape_article_detail(self, article_url):
        """Scraping detail artikel individual"""
        try:
            logger.info(f"Memulai scraping detail artikel: {article_url}")
            
            content = self.get_page_content(article_url)
            if not content:
                return {'author': 'N/A', 'content': 'N/A'}
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Cari penulis
            author_selectors = [
                '.author a', '.writer a', '.byline a',
                '.post-author a', '.article-author a',
                '.meta .author a', '.meta .writer a'
            ]
            
            author = "N/A"
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    author = author_elem.get_text(strip=True)
                    break
            
            # Cari konten artikel
            content_selectors = [
                'article', '.content', '.article-content',
                '.post-content', '.entry-content', '.news-content',
                '.main-content', '.story-content'
            ]
            
            content_text = "N/A"
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Hapus script dan style tags
                    for script in content_elem(["script", "style"]):
                        script.decompose()
                    content_text = content_elem.get_text(strip=True)
                    break
            
            return {
                'author': author,
                'content': content_text
            }
            
        except Exception as e:
            logger.error(f"Error saat scraping detail artikel: {e}")
            return {'author': 'N/A', 'content': 'N/A'}
    
    def search_news_selenium(self, search_query):
        """Mencari berita menggunakan Selenium sebagai fallback"""
        try:
            logger.info(f"Memulai pencarian menggunakan Selenium untuk: {search_query}")
            
            # Buka halaman utama
            self.driver.get(self.base_url)
            time.sleep(5)
            
            # Cari form pencarian dengan berbagai metode
            search_input = None
            search_selectors = [
                "input[type='search']",
                "input[placeholder*='search' i]",
                "input[placeholder*='cari' i]",
                "input[name*='search' i]",
                "input[name*='q']",
                "input[class*='search' i]",
                "input[id*='search' i]"
            ]
            
            for selector in search_selectors:
                try:
                    search_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if search_input:
                        logger.info(f"Input pencarian ditemukan dengan selector: {selector}")
                        break
                except NoSuchElementException:
                    continue
            
            if not search_input:
                logger.error("Input pencarian tidak ditemukan")
                return []
            
            # Input query dan submit
            search_input.clear()
            search_input.send_keys(search_query)
            time.sleep(2)
            search_input.send_keys(Keys.RETURN)
            time.sleep(5)
            
            # Ekstrak hasil pencarian
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            articles = self.extract_articles_from_soup(soup)
            
            logger.info(f"Selenium berhasil menemukan {len(articles)} artikel")
            return articles
            
        except Exception as e:
            logger.error(f"Error dalam pencarian menggunakan Selenium: {e}")
            return []
    
    def scrape_news_complete(self, search_query, max_articles=10):
        """Fungsi utama untuk scraping berita lengkap"""
        try:
            logger.info(f"Memulai scraping berita untuk query: {search_query}")
            
            # Coba metode requests terlebih dahulu
            news_list = self.search_news_requests(search_query)
            
            # Jika tidak ada hasil, coba Selenium
            if not news_list:
                logger.info("Mencoba metode Selenium...")
                news_list = self.search_news_selenium(search_query)
            
            if not news_list:
                logger.warning("Tidak ada berita ditemukan dengan kedua metode")
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
                time.sleep(random.uniform(1, 3))
            
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
    
    def close_driver(self):
        """Tutup driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Driver berhasil ditutup")

def main():
    """Fungsi utama"""
    scraper = RadarSurabayaScraper()
    
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
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    main()