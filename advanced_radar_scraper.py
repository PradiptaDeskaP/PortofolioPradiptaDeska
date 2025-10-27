import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, quote
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
import undetected_chromedriver as uc

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedRadarSurabayaScraper:
    def __init__(self):
        self.base_url = "https://radarsurabaya.jawapos.com/"
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup undetected Chrome driver"""
        try:
            # Coba undetected chromedriver terlebih dahulu
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            
            self.driver = uc.Chrome(options=options)
            logger.info("Undetected Chrome driver berhasil diinisialisasi")
            
        except Exception as e:
            logger.warning(f"Undetected Chrome driver gagal: {e}")
            # Fallback ke Chrome driver biasa
            try:
                chrome_options = Options()
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--disable-plugins")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                logger.info("Chrome driver biasa berhasil diinisialisasi")
                
            except Exception as e2:
                logger.error(f"Error setting up Chrome driver: {e2}")
                raise
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Random delay untuk menghindari deteksi bot"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def search_news(self, search_query):
        """Mencari berita menggunakan Selenium"""
        try:
            logger.info(f"Memulai pencarian untuk: {search_query}")
            
            # Buka halaman utama
            self.driver.get(self.base_url)
            self.random_delay(3, 5)
            
            # Cari input pencarian
            search_input = None
            search_selectors = [
                "input[type='search']",
                "input[placeholder*='search' i]",
                "input[placeholder*='cari' i]",
                "input[name*='search' i]",
                "input[name*='q']",
                "input[class*='search' i]",
                "input[id*='search' i]",
                "input[type='text']"
            ]
            
            for selector in search_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            search_input = element
                            logger.info(f"Input pencarian ditemukan dengan selector: {selector}")
                            break
                    if search_input:
                        break
                except NoSuchElementException:
                    continue
            
            if not search_input:
                logger.warning("Input pencarian tidak ditemukan, mencoba mengambil berita terbaru...")
                return self.get_latest_news()
            
            # Input query dengan simulasi typing manusia
            search_input.clear()
            for char in search_query:
                search_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            self.random_delay(1, 2)
            
            # Submit pencarian
            try:
                search_input.send_keys(Keys.RETURN)
            except:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
                    submit_button.click()
                except:
                    form = search_input.find_element(By.XPATH, "./ancestor::form")
                    form.submit()
            
            self.random_delay(5, 8)
            
            # Ekstrak hasil pencarian
            return self.extract_search_results()
            
        except Exception as e:
            logger.error(f"Error saat melakukan pencarian: {e}")
            return self.get_latest_news()
    
    def get_latest_news(self):
        """Ambil berita terbaru dari halaman utama"""
        try:
            logger.info("Mengambil berita terbaru dari halaman utama...")
            
            # Buka halaman utama
            self.driver.get(self.base_url)
            self.random_delay(5, 8)
            
            return self.extract_search_results()
            
        except Exception as e:
            logger.error(f"Error mengambil berita terbaru: {e}")
            return []
    
    def extract_search_results(self):
        """Ekstrak hasil pencarian"""
        articles = []
        
        try:
            # Tunggu halaman load
            self.random_delay(3, 5)
            
            # Cari artikel dengan berbagai selector
            article_selectors = [
                "a[href*='radarsurabaya.jawapos.com']",
                ".article a", ".news a", ".post a", ".item a",
                "article a", ".content a", ".main a",
                "h1 a", "h2 a", "h3 a", "h4 a"
            ]
            
            article_links = []
            for selector in article_selectors:
                try:
                    links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if links:
                        article_links.extend(links)
                        logger.info(f"Ditemukan {len(links)} link dengan selector: {selector}")
                except NoSuchElementException:
                    continue
            
            # Remove duplicates dan filter
            seen_urls = set()
            unique_links = []
            for link in article_links:
                try:
                    url = link.get_attribute('href')
                    if (url and url not in seen_urls and 
                        'radarsurabaya.jawapos.com' in url and
                        '/tag/' not in url and
                        '/category/' not in url and
                        '/author/' not in url):
                        seen_urls.add(url)
                        unique_links.append(link)
                except:
                    continue
            
            logger.info(f"Total {len(unique_links)} link unik ditemukan")
            
            # Proses setiap link
            for i, link in enumerate(unique_links[:10]):  # Batasi 10 artikel
                try:
                    article_url = link.get_attribute('href')
                    title = link.text.strip()
                    
                    if not title:
                        # Coba cari judul di parent element
                        try:
                            parent = link.find_element(By.XPATH, "./..")
                            title = parent.text.strip()
                        except:
                            pass
                    
                    if title and len(title) > 10:
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
            logger.error(f"Error extracting search results: {e}")
            return []
    
    def scrape_article_detail(self, article_url):
        """Scraping detail artikel"""
        try:
            logger.info(f"Scraping detail: {article_url}")
            
            # Buka halaman artikel
            self.driver.get(article_url)
            self.random_delay(3, 5)
            
            # Cari penulis
            author = "N/A"
            author_selectors = [
                ".author", ".writer", ".byline", ".post-author",
                ".article-author", ".meta .author", ".meta .writer",
                "span[class*='author']", "div[class*='author']",
                "a[class*='author']", "p[class*='author']"
            ]
            
            for selector in author_selectors:
                try:
                    author_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if author_elem and author_elem.is_displayed():
                        author_text = author_elem.text.strip()
                        if author_text and len(author_text) < 100:
                            author = author_text
                            break
                except NoSuchElementException:
                    continue
            
            # Cari konten artikel
            content_text = "N/A"
            content_selectors = [
                "article", ".content", ".article-content", ".post-content",
                ".entry-content", ".news-content", ".main-content", ".story-content",
                ".single-content", ".post-body", ".article-body", ".story-body"
            ]
            
            for selector in content_selectors:
                try:
                    content_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if content_elem and content_elem.is_displayed():
                        content_text = content_elem.text.strip()
                        if content_text and len(content_text) > 100:
                            break
                except NoSuchElementException:
                    continue
            
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
    
    def close_driver(self):
        """Tutup driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Driver berhasil ditutup")

def main():
    """Fungsi utama"""
    scraper = AdvancedRadarSurabayaScraper()
    
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