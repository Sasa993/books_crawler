# books_crawler
A Python script which crawls 'megasrbija' website, looks for recently addded PDF books, IT PDF books, audiobooks or magazines,
and if found, I receive a push notification on my phone, with title, author, published date/time and link to download page.

I've used BeautifulSoup4 for scraping the website and PushBullet API for sending a notification to my phone. This is basically an
automation script and I use cron and anacron (on Linux), where I've schedueled to run this script every day at 12:30PM.
If you are not using a Unix based OS, you can upload this script to a server and automate it to run on it.
