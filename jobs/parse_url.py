import requests
import json
from urllib.parse import urlparse
from tldextract import extract
from bs4 import BeautifulSoup
from datetime import date, timedelta


def get_position_skills(description, skills):
	position_skills = list()
	for skill in skills:
		if skill.skill_name.lower() in description.lower():
			position_skills.append(skill)

	return position_skills


def get_domain_company(url):
	domain = extract(url).domain
	return domain


def get_linkedin_data(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	data = {}

	try:
		company_name = soup.find('a', class_='topcard__org-name-link').text
		data['company'] = company_name.strip()
	except:
		pass

	try:
		posted_date = soup.find('span', class_='posted-time-ago__text').text
		posted_list = posted_date.split()

		if 'hours' in posted_list or 'hour' in posted_list or 'minutes' in posted_list or 'minute' in posted_list:
			posted_date = date.today()
		elif 'day' in posted_list or 'days' in posted_list:
			posted_date = date.today() - timedelta(int(posted_list[0]))
		elif 'week' in posted_list or 'weeks' in posted_list:
			posted_date = date.today() - timedelta(weeks=int(posted_list[0]))
		else:
			posted_date = date.today()

		data['date_opened'] = posted_date
	except:
		pass

	try:
		data['position_title'] = soup.find('h1', class_='topcard__title').text
	except:
		pass

	try:
		job_description_tag = soup.find('div', class_='show-more-less-html__markup')
		data['job_description'] = job_description_tag.text

		if data['job_description']:
			data['job_description_html'] = str(job_description_tag)
	except:
		pass

	return data


def get_indeed_data(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	data = {}

	try:
		company_name = soup.find('div', class_='icl-u-textColor--success').text
		data['company'] = company_name.strip()
	except:
		pass

	try:
		posted_date = soup.find('div', class_='icl-u-textColor--success').next_sibling.text
		posted_list = posted_date.split()

		if 'hours' in posted_list or 'hour' in posted_list or 'minutes' in posted_list or 'minute' in posted_list:
			posted_date = date.today()
		elif 'day' in posted_list or 'days' in posted_list:
			posted_date = date.today() - timedelta(int(posted_list[0]))
		elif 'week' in posted_list or 'weeks' in posted_list:
			posted_date = date.today() - timedelta(weeks=int(posted_list[0]))
		else:
			posted_date = date.today()

		data['date_opened'] = posted_date
	except:
		pass

	try:
		data['position_title'] = soup.find('h1', class_='jobsearch-JobInfoHeader-title').text
	except:
		pass

	try:
		job_description_tag = soup.find('div', id='jobDescriptionText')
		data['job_description'] = job_description_tag.text

		if data['job_description']:
			data['job_description_html'] = str(job_description_tag)

	except:
		pass

	return data


def get_amazon_data(url):
	page = requests.get(url)

	page = page.text.replace('<br/>', ' ')
	soup = BeautifulSoup(page, 'html.parser')

	data = {}

	data['company'] = 'Amazon'

	try:
		data['position_title'] = soup.find('h1', {'class': 'title'}).text
	except:
		pass

	try:
		description = soup.find('div', {'class': 'section description'})
		description = description.find('p')
		data['job_description'] = description.text
	except:
		pass

	return data


def get_job_data(url, company_name):

	domain = get_domain_company(url)

	if domain == 'amazon':
		return get_amazon_data(url)
	elif domain == 'indeed':
		return get_indeed_data(url)
	elif domain == 'linkedin':
		return get_linkedin_data(url)
	else:
		return {}
