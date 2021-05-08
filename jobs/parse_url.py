import requests
import json
from urllib.parse import urlparse
from tldextract import extract
from bs4 import BeautifulSoup


def get_domain_company(url):
	domain = extract(url).domain
	return domain


def get_amazon_data(url):
	company = get_domain_company(url)
	page = requests.get(url)

	page = page.text.replace('<br/>', ' ')
	soup = BeautifulSoup(page, 'html.parser')

	data = {}
	data['company'] = company
	data['position_title'] = soup.find('h1', {'class': 'title'}).text

	description = soup.find('div', {'class': 'section description'})
	description = description.find('p')
	data['job_description'] = description.text

	return data
