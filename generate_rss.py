import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
from zoneinfo import ZoneInfo
import re

# プラットフォーム別のURL定義
platforms = {
    "general": "https://firebase.google.com/support/releases",
    "ios": "https://firebase.google.com/support/release-notes/ios",
    "android": "https://firebase.google.com/support/release-notes/android",
    "js": "https://firebase.google.com/support/release-notes/js",
    "flutter": "https://firebase.google.com/support/release-notes/flutter",
    "cpp": "https://firebase.google.com/support/release-notes/cpp-relnotes",
    "unity": "https://firebase.google.com/support/release-notes/unity",
    "admin-node": "https://firebase.google.com/support/release-notes/admin/node",
    "admin-java": "https://firebase.google.com/support/release-notes/admin/java",
    "admin-python": "https://firebase.google.com/support/release-notes/admin/python",
    "admin-go": "https://firebase.google.com/support/release-notes/admin/go",
    "admin-dotnet": "https://firebase.google.com/support/release-notes/admin/dotnet",
    "security-rules": "https://firebase.google.com/support/release-notes/security-rules",
    "cli": "https://firebase.google.com/support/release-notes/cli"
}

# 共通のRSSフィード生成処理
def generate_feed(url, output_path, platform_name=""):
    # ページを取得
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    if platform_name == "general":
        title_prefix = ""
    else:
        title_prefix = platform_name.capitalize()

    feed_title = f"{title_prefix}Firebase Release Notes"
    if title_prefix:
        feed_title = f"Firebase Release Notes - {title_prefix}"

    # RSSフィードを生成
    fg = FeedGenerator()
    fg.title(feed_title)
    fg.link(href=url)
    fg.description(f'Latest updates and release notes for Firebase{" " + title_prefix if title_prefix else ""}.')
    
    # リリースノートを抽出
    for release in soup.find_all('div', class_='devsite-article-body'):
        subtitles = release.find_all('h2')
        # generalとandroidの場合のみ、最初のサブタイトルをスキップする
        if platform_name == "general" or platform_name == "android":
            releases = subtitles[1:]
        else:
            releases = subtitles
        
        for item in releases:
            fe = fg.add_entry()
            fe.title(item.text)
            fe.link(href=url + '#' + item.get('id', ''))
            
            # 日付を抽出
            try:
                date_object = datetime.strptime(item.text, '%B %d, %Y')
                date_object_with_timezone = date_object.replace(tzinfo=ZoneInfo('UTC'))
                fe.pubDate(date_object_with_timezone.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
            except ValueError:
                # 日付のフォーマットが異なる場合
                pass
            
            # descriptionを生成
            summary = ''
            for sibling in item.find_next_siblings():
                if sibling.name == 'h2':
                    break
                if sibling.name in ['p', 'h3', 'ul']:
                    summary += str(sibling)
            
            fe.summary(summary, type='html')
    
    # RSSフィードを保存
    fg.rss_file(output_path)
    print(f"Generated: {output_path}")

# RSSフィード生成
for platform, platform_url in platforms.items():
    if platform == "general":
        output_path = f'docs/firebase_releases.xml'
    else:
        output_path = f'docs/firebase_releases_{platform}.xml'
    
    generate_feed(platform_url, output_path, platform)