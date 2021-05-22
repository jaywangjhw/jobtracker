import requests

def get_reddit_data(limit, q, sort, subreddit):
	
	print(f'Limit: {limit}, Q: {q}, Sort: {sort}, Subreddit: {subreddit}')

	REDDIT_USERNAME = "Key_River6193"
	REDDIT_PASSWORD = "password123"
	APP_ID = "I26Rkh_33ecfDw"
	APP_SECRET = "m38OHAtJOt1g-LnNBbgWZOR449shbw"

	base_url = 'https://www.reddit.com/'
	data = {'grant_type': 'password', 'username': REDDIT_USERNAME, 'password': REDDIT_PASSWORD}
	auth = requests.auth.HTTPBasicAuth(APP_ID, APP_SECRET)
	headers = {'User-Agent': 'job-tracker/0.0.1 by /u/Key_River619'}

	r = requests.post(base_url + 'api/v1/access_token',
					   data=data,
					   headers=headers,
					   auth=auth)
	 
	ACCESS_TOKEN = r.json()['access_token']
	 
	headers['Authorization'] = f'bearer {ACCESS_TOKEN}'

	restrict = "on"
	
	res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/search?q={q}&sort={sort}&restrict_sr={restrict}&limit={limit}&raw_json=1', headers=headers)
		 
	results = res.json()['data']
	children = results['children']

	results = []
	 
	for data in children:
			
		entry = {}
		 
		content = data['data']
			
		entry['title'] = content['title']
		entry['url'] = content['url']
		entry['body'] = content['selftext_html']
		entry['score'] = content['score']

		results.append(entry)
	
	return results		

def printList(list):
	for item in list:
		print(item)	


