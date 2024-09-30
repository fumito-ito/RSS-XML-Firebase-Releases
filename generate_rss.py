import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
from zoneinfo import ZoneInfo

# FirebaseリリースページのURL
url = 'https://firebase.google.com/support/releases'

# ページを取得
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# RSSフィードを生成
fg = FeedGenerator()
fg.title('Firebase Release Notes')
fg.link(href=url)
fg.description('Latest updates and release notes for Firebase.')

# リリースノートを抽出
for release in soup.find_all('div', class_='devsite-article-body'):
    subtitles = release.find_all('h2')
    # 最初のサブタイトルは `Latest versions of Firebase SDKs and versioned tooling` なので無視する
    releases = subtitles[1:]
    for item in releases:
        fe = fg.add_entry()
        fe.title(item.text)
        fe.link(href=url + '#' + item.get('id'))
        
        # 日付を抽出
        date_object = datetime.strptime(item.text, '%B %d, %Y')
        date_object_with_timezone = date_object.replace(tzinfo=ZoneInfo('UTC'))
        fe.pubDate(date_object_with_timezone.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
        
        # descriptionを生成
        summary = ''
        for sibling in item.find_next_siblings():
            if sibling.name == 'h2':
                break
            if sibling.name in ['p', 'h3', 'ul']:
                summary += str(sibling)
        
        fe.summary(summary, type='html')

# RSSフィードを保存
fg.rss_file('firebase_releases.xml')