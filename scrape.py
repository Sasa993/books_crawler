import argparse
import mechanicalsoup
from datetime import date, timedelta
from settings import url
from utils.calendar import convert_to_target_format
from utils.login import login_to_page
from utils.pushbullet import send_notification

book_types = {
	'audio': '89.0',
	'domestic': '188.0',
	'it': '154.0',
	'magazine': '73.0',
}

parser = argparse.ArgumentParser(description='Todo todo well todo!')

parser.add_argument(
	"--type",
	choices=book_types.keys(),
	type=str,
	required=True,
	help="This is more info."
)
args = parser.parse_args()
full_url = url + book_types[args.type]
# print(1111, full_url, type(full_url))
yesterday = date.today() - timedelta(1)
yesterday = convert_to_target_format(yesterday)
# todo: add logging

def scrape(link, post_starts_at, subject_name):
	"""
	Crawl Megasrbija website and collect desired content.
	Collect only books/magazines that have been published
	day before - yesterday and use Pushbullet to notify user.
	"""
	book_counter = 0
	books_list = {}
	soup = login_to_page(link)
	start = soup.find("div", {"id": "messageindex"}).table.tbody
	# print(222, start)

	for book in start.find_all("tr")[post_starts_at:]:
		lastpost = book.find("td", class_="lastpost").text.split()
		print(333, lastpost)
		# avoid looping through today's published books/magazines
		if ("danas" not in lastpost):
			published_date = f'{lastpost[0]} {lastpost[1]} {lastpost[2].rstrip(",")}'

			if (published_date == yesterday):
				title = book.find("td", class_="subject").div.span.a.text
				published_time = lastpost[3]
				book_link = book.find("td", class_="subject").div.span.a['href']
				books_list[book_counter] = {}
				books_list[book_counter]['title'] = title
				books_list[book_counter]['date'] = published_date
				books_list[book_counter]['time'] = published_time
				books_list[book_counter]['link'] = book_link
				book_counter += 1

	body = ""
	if (book_counter > 0):
		title = f"{book_counter} new {subject_name.title()} book/s added\
			yesterday ({yesterday})!\n"
		for x in range(book_counter):
			body += f"{books_list[x]['title']}\
				({books_list[x]['link']})\n\n"

		send_notification(title, body)

scrape(full_url, 5, args.type)
# scrape('https://megasrbija.com/index.php?board=188.0', 8, 'Domestic Book')
# scrape('https://megasrbija.com/index.php?board=154.0', 7, 'IT Book') # todo: error
# scrape('https://megasrbija.com/index.php?board=73.0', 6, 'Magazine')