# books_crawler
A Python script which crawls 'megasrbija' website, looks for recently addded PDF books, IT PDF books, audiobooks or magazines,
and if found, I receive a push notification on my phone, with title, author, published date/time and link to download page.

I've used BeautifulSoup4 for scraping the website and PushBullet API for sending a notification to my phone. This is basically an
automation script and I use cron and anacron (on Linux), where I've schedueled to run this script every day at 12:30PM.
If you are not using a Unix based OS, you can upload this script to a server and automate it to run on it.


# TODO
- make code more modular -> split it to different util files/modules
- remove "post_starts_at" argument/parameter and find an alternative: maybe those divs which do not have "sticky" class
- write documentation how to use Pushbullet + API
- create main.config file and place Pushbullet API info there + login info
- change body text to something like:
Author: Vanja Bulic
Book: Jovanovo zavestanje
Link: https://megasrbija.com/index.php/topic=131836.0
use char "-" for slicing author and book title