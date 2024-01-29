from bs4 import BeautifulSoup as bs
import requests
import csv


# simple crawler from isna.ir and varzersh3.com that crawls 2500 sport news and 2500 politics news

politics_genres = ['سیاست داخلی', 'سیاسی2', 'بین الملل2', 'ایران در جهان', 'انرژی هسته‎‌ای', 'گزارش و تحلیل',
                   'غرب آسیا و آفریقا', 'محور مقاومت', 'آسیا و اقیانوسیه', 'آمریکا و اروپا', 'دفاعی - امنيتی',
                   'اندیشه امام و رهبری', 'مجلس', 'دولت', 'سیاست خارجی']

sitemaps = ['https://www.isna.ir/sitemap/1402/sitemap.xml',
            'https://www.isna.ir/sitemap/1401/sitemap.xml',
            'https://www.isna.ir/sitemap/1400/sitemap.xml',
            'https://www.isna.ir/sitemap/1399/sitemap.xml',
            'https://www.isna.ir/sitemap/1398/sitemap.xml',
            'https://www.isna.ir/sitemap/1397/sitemap.xml',
            'https://www.isna.ir/sitemap/1396/sitemap.xml',
            'https://www.isna.ir/sitemap/1395/sitemap.xml',
            'https://www.isna.ir/sitemap/1394/sitemap.xml',
            'https://www.isna.ir/sitemap/1393/sitemap.xml',
            'https://www.isna.ir/sitemap/1392/sitemap.xml',
            'https://www.isna.ir/sitemap/1391/sitemap.xml',
            'https://www.isna.ir/sitemap/1390/sitemap.xml',
            'https://www.isna.ir/sitemap/1389/sitemap.xml',
            'https://www.isna.ir/sitemap/1388/sitemap.xml',
            'https://www.isna.ir/sitemap/1387/sitemap.xml',
            'https://www.isna.ir/sitemap/1386/sitemap.xml',
            'https://www.isna.ir/sitemap/1385/sitemap.xml',
            'https://www.isna.ir/sitemap/1384/sitemap.xml',
            'https://www.isna.ir/sitemap/1383/sitemap.xml',
            'https://www.isna.ir/sitemap/1382/sitemap.xml',
            'https://www.isna.ir/sitemap/1381/sitemap.xml',
            'https://www.isna.ir/sitemap/1380/sitemap.xml',
            'https://www.isna.ir/sitemap/1379/sitemap.xml',
            'https://www.isna.ir/sitemap/1378/sitemap.xml'
            ]
news_num = 0
with open('politics.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar=',')
    for year in sitemaps:
        year_archive = requests.get(year)
        soup = bs(year_archive.content, 'xml')
        day_archive = soup.findAll('loc')
        for day in day_archive:
            news = requests.get(day.get_text())
            soup2 = bs(news.content, 'xml')
            links = soup2.find('loc') or []
            for link in links:
                request = requests.get(link)
                soup3 = bs(request.content, 'xml')
                try:
                    genre = soup3.find(attrs={'itemprop': 'articleSection'}).get_text().strip()
                except AttributeError:
                    continue
                if genre in politics_genres:
                    text = soup3.find(attrs={'itemprop': 'articleBody'}).get_text()
                    writer.writerow((link.get_text(), ' '.join(text.split())))
                    news_num += 1
                    if news_num == 2500:
                        exit(0)

current_page = 'https://www.varzesh3.com/sitemap/news'
archive = requests.get(current_page)
soup = bs(archive.content, 'html.parser')
links = soup.findAll('loc')
link_num = 0
with open('sports.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for link in links:
        soup = bs(requests.get(link.get_text()).content, 'html.parser')
        body = soup.find('div', attrs={'class': 'news-text'}).get_text()
        writer.writerow((link.get_text(), ' '.join(body.split())))
        link_num += 1
        if link_num == 2500:
            break
