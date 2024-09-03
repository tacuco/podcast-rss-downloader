# Podcast Downloader

Podcast Downloader is a Python script that automates the process of downloading podcast episodes from RSS feeds. It organizes downloads into podcast-specific folders, handles cover art, and keeps track of previously downloaded episodes to avoid duplicates.

## Features

- Downloads MP3 episodes from podcast RSS feeds
- Downloads podcast cover images
- Organizes downloads into podcast-specific folders
- Sanitizes filenames to remove problematic characters
- Adds date or sequence number to filenames for easy sorting
- Keeps track of downloaded episodes to avoid duplicates
- Handles various date formats in RSS feeds

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository or download the `podcast_downloader.py` script.

2. Install the required Python package:

   ```
   pip install requests
   ```

3. Make the script executable (on Unix-like systems):

   ```
   chmod +x podcast_downloader.py
   ```

## Usage

Run the script from the command line, providing the RSS feed URL as an argument:

```
python podcast_downloader.py <rss_feed_url>
```

For example:

```
python podcast_downloader.py https://example.com/podcast_feed.xml
```

## Output

The script will create a folder for each podcast, named after the podcast title (with special characters removed). Inside this folder, you'll find:

- MP3 files of the podcast episodes, named with the format: `YYYYMMDD_Episode_Title.mp3` or `seqXXXX_Episode_Title.mp3`
- The podcast cover image (if available)
- A `downloaded_episodes.txt` file keeping track of downloaded episodes

The script will print information about the download process, including:

- The podcast title
- Total number of episodes in the feed
- Number of new downloads
- List of newly downloaded episodes

## Notes

- The script uses the publication date of episodes when available. If a date is not available or cannot be parsed, it uses a sequence number instead.
- Filenames are sanitized to remove or replace characters that might cause issues on different file systems.
- The script is designed to be run multiple times on the same feed, only downloading new episodes each time.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/podcast-downloader/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
