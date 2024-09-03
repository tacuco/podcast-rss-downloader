#!/usr/bin/env python3
import os
import sys
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import re
from datetime import datetime
from email.utils import parsedate_to_datetime

def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.encode('ascii', 'ignore').decode('ascii')
    return filename[:255]

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def parse_date(date_string):
    if not date_string:
        return None
    try:
        return parsedate_to_datetime(date_string)
    except:
        formats = [
            '%a, %d %b %Y %H:%M:%S %Z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
            '%a, %d %b %Y %H:%M:%S %z',
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
    return None

def parse_rss(rss_url):
    response = requests.get(rss_url)
    root = ET.fromstring(response.content)
    channel = root.find('channel')
    
    podcast_title = channel.find('title').text
    episodes = []
    
    for item in channel.findall('item'):
        title = item.find('title').text
        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else None
        enclosure = item.find('enclosure')
        if enclosure is not None and enclosure.get('type') == 'audio/mpeg':
            mp3_url = enclosure.get('url')
            episodes.append({'title': title, 'url': mp3_url, 'date': pub_date})
    
    episodes.sort(key=lambda x: parse_date(x['date']) or datetime.max, reverse=True)
    
    image_url = channel.find('image/url').text if channel.find('image/url') is not None else None
    
    return podcast_title, episodes, image_url

def main(input_url):
    if os.path.isfile(input_url):
        with open(input_url, 'r') as f:
            rss_url = f.read().strip()
    else:
        rss_url = input_url

    podcast_title, episodes, image_url = parse_rss(rss_url)
    
    podcast_dir = sanitize_filename(podcast_title)
    os.makedirs(podcast_dir, exist_ok=True)
    
    # Save the podcast URL
    url_file = os.path.join(podcast_dir, 'podcast_url.txt')
    with open(url_file, 'w') as f:
        f.write(rss_url)
    
    # Download cover image if it doesn't exist
    if image_url:
        image_ext = os.path.splitext(urlparse(image_url).path)[1]
        image_filename = os.path.join(podcast_dir, f'cover{image_ext}')
        if not os.path.exists(image_filename):
            download_file(image_url, image_filename)
            print(f"Downloaded cover image: {image_filename}")
        else:
            print(f"Cover image already exists: {image_filename}")
    
    downloaded_file = os.path.join(podcast_dir, 'downloaded_episodes.txt')
    if os.path.exists(downloaded_file):
        with open(downloaded_file, 'r') as f:
            downloaded_episodes = set(line.strip() for line in f)
    else:
        downloaded_episodes = set()
    
    new_downloads = []
    sequence_number = 1
    for episode in episodes:
        if episode['url'] not in downloaded_episodes:
            parsed_date = parse_date(episode['date'])
            if parsed_date:
                date_str = parsed_date.strftime('%Y%m%d')
            else:
                date_str = f'seq{sequence_number:04d}'
                sequence_number += 1
            
            safe_title = sanitize_filename(episode['title'])
            filename = os.path.join(podcast_dir, f"{date_str}_{safe_title}.mp3")
            
            try:
                download_file(episode['url'], filename)
                downloaded_episodes.add(episode['url'])
                new_downloads.append(filename)
                print(f"Downloaded: {filename}")
                
                # Update downloaded_episodes.txt after each successful download
                with open(downloaded_file, 'a') as f:
                    f.write(episode['url'] + '\n')
            except Exception as e:
                print(f"Error downloading {episode['title']}: {str(e)}")
    
    print(f"\nPodcast: {podcast_title}")
    print(f"Total episodes: {len(episodes)}")
    print(f"New downloads: {len(new_downloads)}")
    print("New episodes downloaded:")
    for download in new_downloads:
        print(download)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python podcast_downloader.py <rss_feed_url_or_file>")
        sys.exit(1)
    
    main(sys.argv[1])
