import requests
import json
from urllib.parse import urlparse
from tldextract import extract
from bs4 import BeautifulSoup
from datetime import date, timedelta


def get_domain_company(url):
	domain = extract(url).domain
	return domain


def get_linkedin_data(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	data = {}

	try:
		data['company'] = soup.find('a', class_='topcard__org-name-link').text
	except:
		pass

	try:
		posted_date = soup.find('span', class_='posted-time-ago__text').text
		posted_list = posted_date.split()
		if 'days' in posted_list:
			print(posted_list)

		if 'hours' in posted_list or 'hour' in posted_list or 'minutes' in posted_list or 'minute' in posted_list:
			posted_date = date.today()
		elif 'day' in posted_list or 'days' in posted_list:
			posted_date = date.today() - timedelta(int(posted_list[0]))
		elif 'week' in posted_list or 'weeks' in posted_list:
			posted_date = date.today() - timedelta(weeks=int(posted_list[0]))

		data['date_opened'] = posted_date
	except:
		pass

	try:
		data['position_title'] = soup.find('h1', class_='topcard__title').text
	except:
		pass

	try:
		data['job_description_html'] = str(soup.find('div', class_='show-more-less-html__markup'))
		data['job_description'] = soup.find('div', class_='show-more-less-html__markup').text
	except:
		pass

	return data


def get_indeed_data(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	data = {}

	try:
		data['company'] = soup.find('a', class_='topcard__org-name-link').text
	except:
		pass

	try:
		posted_date = soup.find('span', class_='posted-time-ago__text').text
		posted_list = posted_date.split()
		if 'days' in posted_list:
			print(posted_list)

		if 'hours' in posted_list or 'hour' in posted_list or 'minutes' in posted_list or 'minute' in posted_list:
			posted_date = date.today()
		elif 'day' in posted_list or 'days' in posted_list:
			posted_date = date.today() - timedelta(int(posted_list[0]))
		elif 'week' in posted_list or 'weeks' in posted_list:
			posted_date = date.today() - timedelta(weeks=int(posted_list[0]))

		data['date_opened'] = posted_date
	except:
		pass

	try:
		data['position_title'] = soup.find('h1', class_='topcard__title').text
	except:
		pass

	try:
		data['job_description_html'] = str(soup.find('div', class_='show-more-less-html__markup'))
		data['job_description'] = soup.find('div', class_='show-more-less-html__markup').text
	except:
		pass

	return data


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

	domain = get_domain_company(url)

	if company_name and company_name.lower() == 'amazon':
		return get_amazon_data(url)
	elif domain == 'indeed':
		return get_indeed_data(url)
	elif domain == 'linkedin':
		return get_linkedin_data(url)
	else:
		return {}
