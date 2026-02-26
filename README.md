# appstore-reviews-scraper
A Python script to scrape Apple App Store reviews via the public RSS feed and export them to Excel.


## Features
- Fetch App Store reviews using Apple's public RSS (XML) feed
- Supports pagination (most recent reviews first)
- Extracts:
  - username
  - publish date
  - rating
  - review title
  - review content
- Saves results as an Excel file (`.xlsx`)

## Requirements
- Python 3.9+
- requests
- pandas
- lxml
- openpyxl

## Installation
Install dependencies with:

pip install -r requirements.txt


### Usage

Edit the configuration section in commentsE.py:

APP_URL = "https://apps.apple.com/us/app/meitu-ai-photo-video-editor/id416048305" 
#Chang URL in to the app id you want to scrape
#This URL from appstore the app page
COUNTRY = "gb"
MAX_PAGES = 10
OUTPUT_FILE = "Comment_reviews.xlsx"

Then run:

python commentsE.py



### Using Other Apps

This project uses Meitu as a demonstration example.

To scrape reviews for other apps, simply replace APP_URL with:

another App Store URL (the numeric id at the end will be extracted automatically), or

a pure App ID (digits only)

No other code changes are required.

Notes

Apple RSS feeds have a public limit (typically up to ~500 reviews).

Please avoid sending requests too frequently; this script includes a short delay between pages.

This project is intended for learning and research purposes.
