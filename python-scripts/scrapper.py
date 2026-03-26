from bs4 import BeautifulSoup
import requests
url = "https://www.scrapethissite.com/pages/simple/"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

print(soup.prettify())