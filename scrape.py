#!/usr/bin/python3.6
from bs4 import BeautifulSoup
from datetime import date, timedelta
import requests, json

yesterday = date.today() - timedelta(1)

# Python doesn't have a switch-case statement, therefore, I had to create a custom swtich-case function
def switch_month(x):
	return {
		'Januar': '01',
		'Februar': '02',
		'Mart': '03',
		'April': '04',
		'Maj': '05',
		'Jun': '06',
		'Jul': '07',
		'Avgust': '08',
		'Septembar': '09',
		'Oktobar': '10',
		'Novembar': '11',
		'Decembar': '12',
		'danas': '13'
	}[x]

# Sending notification via pushbullet
def send_notification_via_pushbullet(title, body):
    data_send = {"type": "note", "title": title, "body": body}
 
    ACCESS_TOKEN = 'o.ibjaaNgt1q4UyKJ3Tbpn6e8t9RDVVFlT'
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')

def scrape(link, post_starts_at, subject_name):
	book_counter = 0
	books_list = {}

	source = requests.get(link).text
	soup = BeautifulSoup(source, 'lxml')

	start = soup.find("div", {"id": "messageindex"}).table.tbody

	for book in start.find_all("tr")[post_starts_at:]:
		lastpost = book.find("td", class_="lastpost").text
		# we don't care about today's published books/magazines, so we are avoiding looping through it if 'danas' is available
		if ("danas" not in lastpost):	
			# slicing it to get a date format "year-month-day" so that I could compare it with yesterday's date
			published_date = str(yesterday.year) + "-" + switch_month(lastpost.split()[1]) + "-" + lastpost.split()[0]

			if (published_date == str(yesterday)):
				title = book.find("td", class_="subject").div.span.a.text
				published_time = lastpost.split()[3]
				link = book.find("td", class_="subject").div.span.a['href']

				books_list[book_counter] = {}
				books_list[book_counter]['title'] = title
				books_list[book_counter]['published_date'] = published_date
				books_list[book_counter]['published_time'] = published_time
				books_list[book_counter]['link'] = link

				book_counter += 1
		# else:
		# 	break

	final_message = ""

	if (book_counter > 0):
		for x in range(book_counter):
			final_message += "{0} Title: {1} -- uploaded on {2} at {3} ({4}) \n".format(subject_name, books_list[x]['title'], books_list[x]['published_date'], books_list[x]['published_time'], books_list[x]['link'])

		send_notification_via_pushbullet("There are {0} new {1}/s added yesterday!".format(book_counter, subject_name), final_message)
		# print(final_message)

scrape('https://megasrbija.com/index.php?board=89.0', 7, 'Audio Book')
scrape('https://megasrbija.com/index.php?board=71.0', 10, 'Domestic Book')
scrape('https://megasrbija.com/index.php?board=102.0', 6, 'IT Book')
scrape('https://megasrbija.com/index.php?board=73.0', 5, 'Magazine')