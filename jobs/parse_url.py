import requests
import json
from urllib.parse import urlparse
from tldextract import extract
from bs4 import BeautifulSoup


def get_domain_company(url):
	domain = extract(url).domain
	return domain


def get_amazon_data(url):
	data = {}
	company = get_domain_company(url)
	
	if company != 'amazon':
		return data

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


def get_job_data(url, company_name):
	print(url)
	print(company_name)
	if company_name and company_name.lower() == 'amazon':
		return get_amazon_data(url)
	elif get_domain_company(url) == 'amazon':
		return get_amazon_data(url)
	else:
		return {}
