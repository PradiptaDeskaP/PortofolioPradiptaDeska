"""
Tribunnews Surabaya News Scraper
Developed by: Data Engineer & AI Engineer
Version: 1.0

Script ini melakukan scraping berita dari Surabaya Tribunnews berdasarkan keyword yang diinput user.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re
from datetime import datetime
from urllib.parse import quote_plus, urljoin
import sys
import os


class TribunnewsScraper:
    """
    Class untuk melakukan scraping berita dari Surabaya Tribunnews
    """
    
    def __init__(self):
        self.base_url = "https://surabaya.tribunnews.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.results = []
        
    def build_search_url(self, keyword):
        """
        Membuat URL search berdasarkan keyword
        
        Args:
            keyword (str): Keyword pencarian
            
        Returns:
            str: URL search yang sudah diformat
        """
        encoded_keyword = quote_plus(keyword)
        search_url = f"{self.base_url}/search?q={encoded_keyword}&cx=partner-pub-b6469b1ee236d402a&cof=FORID%3A10&ie=UTF-8&siteurl=www.tribunnews.com"
        return search_url
    
    def get_search_results(self, keyword, max_pages=3):
        """
        Mengambil hasil pencarian berita berdasarkan keyword
        
        Args:
            keyword (str): Keyword pencarian
            max_pages (int): Maksimal jumlah halaman yang akan di-scrape
            
        Returns:
            list: List berisi dictionary dengan judul dan URL berita
        """
        print(f"\n🔍 Mencari berita dengan keyword: '{keyword}'")
        print("=" * 80)
        
        articles = []
        page = 0
        
        while page < max_pages:
            if page == 0:
                search_url = self.build_search_url(keyword)
            else:
                # Untuk halaman berikutnya, tambahkan parameter start
                start_param = page * 10
                encoded_keyword = quote_plus(keyword)
                search_url = f"{self.base_url}/search?q={encoded_keyword}&cx=partner-pub-b6469b1ee236d402a&cof=FORID%3A10&ie=UTF-8&siteurl=www.tribunnews.com&start={start_param}"
            
            print(f"\n📄 Mengakses halaman {page + 1}: {search_url}")
            
            try:
                response = self.session.get(search_url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Mencari semua link berita dengan class "gs-title"
                article_links = soup.find_all('a', class_='gs-title')
                
                if not article_links:
                    print(f"⚠️  Tidak ada artikel ditemukan di halaman {page + 1}")
                    break
                
                print(f"✅ Ditemukan {len(article_links)} artikel di halaman {page + 1}")
                
                for idx, link in enumerate(article_links, 1):
                    title = link.get_text(strip=True)
                    url = link.get('href')
                    
                    if url and title:
                        articles.append({
                            'title': title,
                            'url': url
                        })
                        print(f"   {idx}. {title[:80]}...")
                
                page += 1
                time.sleep(2)  # Delay untuk menghindari rate limiting
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Error saat mengakses halaman {page + 1}: {str(e)}")
                break
        
        print(f"\n📊 Total artikel ditemukan: {len(articles)}")
        return articles
    
    def clean_text(self, text):
        """
        Membersihkan teks dari whitespace berlebih dan karakter tidak perlu
        
        Args:
            text (str): Teks yang akan dibersihkan
            
        Returns:
            str: Teks yang sudah dibersihkan
        """
        if not text:
            return ""
        
        # Hapus whitespace berlebih
        text = re.sub(r'\s+', ' ', text)
        # Hapus whitespace di awal dan akhir
        text = text.strip()
        return text
    
    def extract_article_details(self, url):
        """
        Mengekstrak detail artikel dari URL berita
        
        Args:
            url (str): URL artikel berita
            
        Returns:
            dict: Dictionary berisi detail artikel (tanggal, penulis, editor, konten)
        """
        details = {
            'publish_date': '',
            'author': '',
            'editor': '',
            'content': ''
        }
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # 1. Ekstrak tanggal publish
            date_div = soup.find('div', class_='grey bdr3 pb10 pt10')
            if date_div:
                time_tag = date_div.find('time')
                if time_tag:
                    date_span = time_tag.find('span')
                    if date_span:
                        details['publish_date'] = self.clean_text(date_span.get_text())
            
            # 2. Ekstrak penulis dan editor
            credit_div = soup.find('div', class_='credit')
            if credit_div:
                penulis_h5 = credit_div.find('h5', id='penulis')
                if penulis_h5:
                    # Ekstrak penulis
                    author_parts = penulis_h5.find_all('b')
                    if len(author_parts) >= 1:
                        author_link = author_parts[0].find('a')
                        if author_link:
                            details['author'] = self.clean_text(author_link.get_text())
                    
                    # Ekstrak editor
                    if len(author_parts) >= 2:
                        editor_link = author_parts[1].find('a')
                        if editor_link:
                            details['editor'] = self.clean_text(editor_link.get_text())
            
            # 3. Ekstrak konten berita (hanya teks)
            content_div = soup.find('div', class_='side-article txt-article multi-fontsize editcontent')
            if content_div:
                # Hapus elemen yang tidak perlu (iklan, script, dll)
                for unwanted in content_div.find_all(['script', 'style', 'iframe', 'div']):
                    if unwanted.get('class'):
                        # Hapus div yang berisi iklan
                        if any(cls in ['reserved_box_ads', 'baca'] for cls in unwanted.get('class', [])):
                            unwanted.decompose()
                            continue
                    # Jika div memiliki id yang mengandung 'ads' atau 'google'
                    if unwanted.get('id') and ('ads' in unwanted.get('id', '').lower() or 'google' in unwanted.get('id', '').lower()):
                        unwanted.decompose()
                        continue
                
                # Ambil semua paragraf
                paragraphs = content_div.find_all(['p', 'blockquote', 'h1', 'h2', 'h3'])
                content_text = []
                
                for para in paragraphs:
                    # Skip paragraf yang berisi class 'baca' (link baca juga)
                    if para.get('class') and 'baca' in para.get('class', []):
                        continue
                    
                    text = para.get_text(separator=' ', strip=True)
                    text = self.clean_text(text)
                    
                    if text and len(text) > 10:  # Filter teks yang terlalu pendek
                        content_text.append(text)
                
                details['content'] = '\n\n'.join(content_text)
            
        except requests.exceptions.RequestException as e:
            print(f"      ❌ Error saat mengakses artikel: {str(e)}")
        except Exception as e:
            print(f"      ❌ Error saat parsing artikel: {str(e)}")
        
        return details
    
    def scrape_articles(self, keyword, max_pages=3, max_articles=None):
        """
        Melakukan scraping lengkap untuk keyword tertentu
        
        Args:
            keyword (str): Keyword pencarian
            max_pages (int): Maksimal jumlah halaman hasil search yang akan di-scrape
            max_articles (int): Maksimal jumlah artikel yang akan di-scrape (None = semua)
            
        Returns:
            list: List berisi dictionary dengan semua data artikel
        """
        # Reset results
        self.results = []
        
        # Dapatkan daftar artikel dari hasil pencarian
        articles = self.get_search_results(keyword, max_pages)
        
        if not articles:
            print("\n⚠️  Tidak ada artikel ditemukan untuk keyword tersebut.")
            return []
        
        # Batasi jumlah artikel jika max_articles ditentukan
        if max_articles:
            articles = articles[:max_articles]
        
        print(f"\n🚀 Mulai scraping detail dari {len(articles)} artikel...")
        print("=" * 80)
        
        # Scrape detail setiap artikel
        for idx, article in enumerate(articles, 1):
            print(f"\n[{idx}/{len(articles)}] Scraping: {article['title'][:60]}...")
            print(f"      URL: {article['url']}")
            
            # Ekstrak detail artikel
            details = self.extract_article_details(article['url'])
            
            # Gabungkan dengan data artikel
            result = {
                'no': idx,
                'keyword': keyword,
                'title': article['title'],
                'url': article['url'],
                'publish_date': details['publish_date'],
                'author': details['author'],
                'editor': details['editor'],
                'content': details['content'],
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.results.append(result)
            
            # Tampilkan ringkasan
            print(f"      ✅ Tanggal: {details['publish_date']}")
            print(f"      ✅ Penulis: {details['author']}")
            print(f"      ✅ Editor: {details['editor']}")
            print(f"      ✅ Konten: {len(details['content'])} karakter")
            
            # Delay untuk menghindari rate limiting
            time.sleep(3)
        
        print(f"\n✅ Selesai! Total {len(self.results)} artikel berhasil di-scrape.")
        return self.results
    
    def save_to_csv(self, filename=None):
        """
        Menyimpan hasil scraping ke file CSV
        
        Args:
            filename (str): Nama file CSV (default: tribunnews_YYYY-MM-DD_HH-MM-SS.csv)
        """
        if not self.results:
            print("⚠️  Tidak ada data untuk disimpan.")
            return
        
        if not filename:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"tribunnews_{timestamp}.csv"
        
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n💾 Data berhasil disimpan ke: {filename}")
        print(f"   Total baris: {len(df)}")
        print(f"   Ukuran file: {os.path.getsize(filename) / 1024:.2f} KB")
    
    def save_to_json(self, filename=None):
        """
        Menyimpan hasil scraping ke file JSON
        
        Args:
            filename (str): Nama file JSON (default: tribunnews_YYYY-MM-DD_HH-MM-SS.json)
        """
        if not self.results:
            print("⚠️  Tidak ada data untuk disimpan.")
            return
        
        if not filename:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"tribunnews_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Data berhasil disimpan ke: {filename}")
        print(f"   Total artikel: {len(self.results)}")
        print(f"   Ukuran file: {os.path.getsize(filename) / 1024:.2f} KB")
    
    def display_summary(self):
        """
        Menampilkan ringkasan hasil scraping
        """
        if not self.results:
            print("⚠️  Tidak ada data untuk ditampilkan.")
            return
        
        print("\n" + "=" * 80)
        print("📊 RINGKASAN HASIL SCRAPING")
        print("=" * 80)
        print(f"Total Artikel      : {len(self.results)}")
        print(f"Keyword            : {self.results[0]['keyword']}")
        print(f"Waktu Scraping     : {self.results[0]['scraped_at']}")
        
        # Statistik penulis
        authors = [r['author'] for r in self.results if r['author']]
        if authors:
            print(f"\nTotal Penulis Unik : {len(set(authors))}")
        
        # Statistik konten
        total_chars = sum(len(r['content']) for r in self.results)
        avg_chars = total_chars / len(self.results) if self.results else 0
        print(f"\nTotal Karakter     : {total_chars:,}")
        print(f"Rata-rata per Artikel: {avg_chars:,.0f} karakter")
        
        print("=" * 80)


def main():
    """
    Fungsi utama untuk menjalankan scraper
    """
    print("=" * 80)
    print("🚀 TRIBUNNEWS SURABAYA NEWS SCRAPER")
    print("=" * 80)
    print("📰 Scraper berita dari surabaya.tribunnews.com")
    print("🔍 Scraping berdasarkan keyword pencarian")
    print("=" * 80)
    
    # Inisialisasi scraper
    scraper = TribunnewsScraper()
    
    try:
        # Input keyword dari user
        print("\n📝 Masukkan keyword berita yang ingin Anda cari:")
        print("   Contoh: jagung, harga pangan, pemilu, dll")
        keyword = input("   Keyword: ").strip()
        
        if not keyword:
            print("❌ Keyword tidak boleh kosong!")
            sys.exit(1)
        
        # Input jumlah halaman
        print("\n📄 Berapa halaman hasil search yang ingin di-scrape?")
        print("   (1 halaman ≈ 10 artikel, default: 3)")
        max_pages_input = input("   Jumlah halaman [3]: ").strip()
        max_pages = int(max_pages_input) if max_pages_input else 3
        
        # Input maksimal artikel
        print("\n📊 Maksimal berapa artikel yang ingin di-scrape?")
        print("   (Kosongkan untuk scrape semua artikel)")
        max_articles_input = input("   Maksimal artikel [semua]: ").strip()
        max_articles = int(max_articles_input) if max_articles_input else None
        
        # Mulai scraping
        print("\n" + "=" * 80)
        print("🚀 MEMULAI PROSES SCRAPING...")
        print("=" * 80)
        
        start_time = time.time()
        results = scraper.scrape_articles(keyword, max_pages, max_articles)
        end_time = time.time()
        
        if not results:
            print("\n⚠️  Scraping selesai tanpa hasil.")
            sys.exit(0)
        
        # Tampilkan ringkasan
        scraper.display_summary()
        
        # Simpan hasil
        print("\n" + "=" * 80)
        print("💾 MENYIMPAN HASIL SCRAPING...")
        print("=" * 80)
        
        scraper.save_to_csv()
        scraper.save_to_json()
        
        # Waktu eksekusi
        duration = end_time - start_time
        print(f"\n⏱️  Waktu eksekusi: {duration:.2f} detik ({duration/60:.2f} menit)")
        
        print("\n" + "=" * 80)
        print("✅ SCRAPING SELESAI!")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping dibatalkan oleh user.")
        if scraper.results:
            print("💾 Menyimpan hasil scraping yang sudah didapat...")
            scraper.save_to_csv()
            scraper.save_to_json()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
