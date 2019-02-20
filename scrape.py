from bs4 import BeautifulSoup
import requests

source = requests.get('https://megasrbija.com/index.php?board=89.0').text

soup = BeautifulSoup(source, 'lxml')

print(soup.prettify())