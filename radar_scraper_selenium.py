"""
Radar Surabaya News Scraper - Selenium Version
===============================================
Alternative scraper menggunakan Selenium untuk website dengan dynamic content
Lebih lambat tapi lebih reliable untuk website dengan heavy JavaScript

INSTALASI TAMBAHAN:
pip install selenium webdriver-manager
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime
from urllib.parse import quote_plus
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('radar_scraper_selenium.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RadarSurabayaSeleniumScraper:
    """
    Selenium-based scraper untuk Radar Surabaya
    Cocok untuk website dengan dynamic content atau anti-bot protection
    """
    
    def __init__(self, headless=True):
        """
        Initialize scraper dengan Selenium WebDriver
        
        Args:
            headless: Jalankan browser tanpa GUI (default: True)
        """
        self.base_url = "https://radarsurabaya.jawapos.com"
        self.search_url = f"{self.base_url}/search"
        self.results = []
        self.headless = headless
        self.driver = None
        
    def _init_driver(self):
        """Initialize Chrome WebDriver dengan options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        logger.info("Chrome WebDriver initialized")
    
    def search_news(self, keyword, max_pages=5):
        """
        Scrape berita berdasarkan keyword menggunakan Selenium
        
        Args:
            keyword: Keyword pencarian
            max_pages: Maksimal halaman yang di-scrape
            
        Returns:
            List of dictionaries berisi data berita
        """
        try:
            self._init_driver()
            logger.info(f"Memulai scraping dengan keyword: '{keyword}'")
            
            self.results = []
            encoded_keyword = quote_plus(keyword)
            
            for page in range(1, max_pages + 1):
                try:
                    # Build URL
                    if page == 1:
                        url = f"{self.search_url}?q={encoded_keyword}"
                    else:
                        url = f"{self.search_url}?q={encoded_keyword}&page={page}"
                    
                    logger.info(f"Mengakses halaman {page}: {url}")
                    self.driver.get(url)
                    
                    # Wait for content to load
                    time.sleep(2)
                    
                    # Get page source
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    
                    # Extract articles
                    articles = self._extract_search_results(soup)
                    
                    if not articles:
                        logger.info(f"Tidak ada artikel di halaman {page}")
                        break
                    
                    logger.info(f"Ditemukan {len(articles)} artikel di halaman {page}")
                    
                    # Scrape details
                    for idx, article in enumerate(articles, 1):
                        logger.info(f"Scraping detail artikel {idx}/{len(articles)}")
                        detail = self._scrape_article_detail_selenium(article['url'])
                        
                        if detail:
                            article.update(detail)
                            self.results.append(article)
                        
                        time.sleep(1)
                    
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error pada halaman {page}: {e}")
                    break
            
            logger.info(f"Scraping selesai! Total: {len(self.results)} artikel")
            return self.results
            
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed")
    
    def _extract_search_results(self, soup):
        """Extract artikel dari halaman pencarian"""
        articles = []
        
        # Cari containers
        containers = soup.select('div.latest__wrap > div')
        if not containers:
            containers = soup.select('article.latest')
        if not containers:
            containers = soup.select('div.latest')
        
        for container in containers:
            try:
                article = {}
                
                # Title & URL
                title_elem = (container.select_one('h2 > a') or 
                             container.select_one('h2 a') or
                             container.select_one('.latest__right h2 a'))
                
                if not title_elem:
                    continue
                
                article['title'] = title_elem.get_text(strip=True)
                article['url'] = title_elem.get('href', '')
                if not article['url'].startswith('http'):
                    article['url'] = self.base_url + article['url']
                
                # Date
                date_elem = (container.select_one('date') or 
                            container.select_one('time') or
                            container.select_one('.latest__right date'))
                article['date'] = date_elem.get_text(strip=True) if date_elem else 'Unknown'
                
                # Category
                cat_elem = (container.select_one('h4 > a') or
                           container.select_one('h4 a') or
                           container.select_one('.latest__right h4 a'))
                article['category'] = cat_elem.get_text(strip=True) if cat_elem else 'Unknown'
                
                # Excerpt
                excerpt_elem = container.select_one('p')
                article['excerpt'] = excerpt_elem.get_text(strip=True) if excerpt_elem else ''
                
                articles.append(article)
                
            except Exception as e:
                logger.warning(f"Error extracting article: {e}")
                continue
        
        return articles
    
    def _scrape_article_detail_selenium(self, url):
        """Scrape detail artikel menggunakan Selenium"""
        try:
            self.driver.get(url)
            time.sleep(2)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            detail = {}
            
            # Author
            author_elem = (soup.select_one('div.read__info__author > a') or
                          soup.select_one('div.read__info__author a') or
                          soup.select_one('.read__info__author a') or
                          soup.select_one('a[rel="author"]'))
            
            if author_elem:
                detail['author'] = author_elem.get_text(strip=True)
            else:
                author_meta = soup.select_one('meta[name="author"]')
                detail['author'] = author_meta.get('content', 'Unknown') if author_meta else 'Unknown'
            
            # Content
            content_elem = (soup.select_one('div.col-bs10-7 > div') or
                           soup.select_one('div.read__content') or
                           soup.select_one('article div[itemprop="articleBody"]') or
                           soup.select_one('.entry-content'))
            
            if content_elem:
                for unwanted in content_elem.select('script, style, iframe, .ads'):
                    unwanted.decompose()
                
                paragraphs = content_elem.find_all(['p', 'div'], recursive=True)
                content_texts = [p.get_text(strip=True) for p in paragraphs 
                               if p.get_text(strip=True) and len(p.get_text(strip=True)) > 20]
                detail['content'] = '\n\n'.join(content_texts)
            else:
                detail['content'] = 'Content not found'
            
            # Published datetime
            pub_elem = soup.select_one('time[datetime]')
            if pub_elem:
                detail['published_datetime'] = pub_elem.get('datetime', '')
            
            return detail
            
        except Exception as e:
            logger.error(f"Error scraping detail from {url}: {e}")
            return None
    
    def save_to_csv(self, filename=None):
        """Save results to CSV"""
        if not self.results:
            logger.warning("No data to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"radar_surabaya_selenium_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['title', 'url', 'date', 'category', 'author', 
                            'excerpt', 'content', 'published_datetime']
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(self.results)
            
            logger.info(f"Data saved to {filename}")
            print(f"\n✓ Data saved: {filename}")
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
    
    def save_to_json(self, filename=None):
        """Save results to JSON"""
        if not self.results:
            logger.warning("No data to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"radar_surabaya_selenium_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Data saved to {filename}")
            print(f"✓ Data saved: {filename}")
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")


def main():
    """Main function"""
    print("="*80)
    print("RADAR SURABAYA SCRAPER - SELENIUM VERSION")
    print("Cocok untuk website dengan dynamic content")
    print("="*80)
    
    keyword = input("\nMasukkan keyword: ").strip()
    if not keyword:
        print("Error: Keyword required!")
        return
    
    try:
        max_pages = int(input("Jumlah halaman (default: 3): ").strip() or "3")
    except ValueError:
        max_pages = 3
    
    headless_input = input("Jalankan headless? (Y/n): ").strip().lower()
    headless = headless_input != 'n'
    
    print(f"\n🚀 Starting Selenium scraper...")
    print(f"   Keyword: {keyword}")
    print(f"   Pages: {max_pages}")
    print(f"   Headless: {headless}")
    print("\n⏳ Please wait, this may take several minutes...\n")
    
    scraper = RadarSurabayaSeleniumScraper(headless=headless)
    results = scraper.search_news(keyword, max_pages=max_pages)
    
    if not results:
        print("\n❌ No articles found")
        return
    
    print(f"\n✓ Successfully scraped {len(results)} articles")
    
    # Save
    scraper.save_to_csv()
    scraper.save_to_json()
    
    print("\n" + "="*80)
    print("✓ SCRAPING COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.error(f"Fatal error: {e}", exc_info=True)
