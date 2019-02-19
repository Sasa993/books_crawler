from bs4 import BeautifulSoup
import requests, datetime, json

now = datetime.datetime.now().date()

book_counter = 0
books_list = {}

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
		'Decembar': '12'
	}[x]

def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}
 
    ACCESS_TOKEN = 'o.ibjaaNgt1q4UyKJ3Tbpn6e8t9RDVVFlT'
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print ('Sent.')

source = requests.get('https://megasrbija.com/index.php?board=89.0').text
soup = BeautifulSoup(source, 'lxml')

start = soup.find("div", {"id": "messageindex"}).table.tbody

for knjiga in start.find_all("tr")[7:]:
	lastpost = knjiga.find("td", class_="lastpost windowbg2").text
	# slicing it to get a date format "year-month-day" so that I could compare it with today's date
	published_date = str(now.year) + "-" + switch_month(lastpost.split()[1]) + "-" + lastpost.split()[0]

	if (published_date == str(now)):
		title = knjiga.find("td", class_="subject windowbg2").div.span.a.text
		published_time = lastpost.split()[3]
		link = knjiga.find("td", class_="subject windowbg2").div.span.a['href']

		books_list[book_counter] = {}
		books_list[book_counter]['title'] = title
		books_list[book_counter]['published_date'] = published_date
		books_list[book_counter]['published_time'] = published_time
		books_list[book_counter]['link'] = link

		book_counter += 1
	else:
		break

final_message = ""

for x in range(book_counter):
	final_message += "Book Title: {0} -- uploaded on {1} at {2} ({3}) \n".format(books_list[x]['title'], books_list[x]['published_date'], books_list[x]['published_time'], books_list[x]['link'])

send_notification_via_pushbullet("There are {0} new audio books added today!".format(book_counter), final_message)