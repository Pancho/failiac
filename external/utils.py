import logging
import json
import time
import urllib.request
import urllib.parse


import numpy


logger = logging.getLogger(__name__)
DATE_FORMATS = [
	'%Y-%m-%d',
	'%Y/%m/%d',
	'%B %d, %Y',
	'%b %d, %Y',
	'%d %B %Y',
	'%d. %B %Y',
]

# Used these to harvest as many birth dates as possible
DATE_ANOMALIES = {
	'T08:30': '',
	'T15:30': '',
	'T00:00:00': '',
	'T16:00': '',
	'T13:25': '',
	'T17:55Z': '',
	'T06:19': '',
	'T23:55': '',
	'T01:51': '',
	'T20:44': '',
	'T23:19': '',
	'T04:11Z': '',
	'T04:45': '',
	'T09:03+01:00': '',
	'T19:46': '',
	'T09': '',
	'T23:30Z': '',
	'T12:13': '',
}
FREEBASE_API_KEY = 'Your Google API Key Here'
FREEBASE_API_ENDPOINT = 'https://www.googleapis.com/freebase/v1/mqlread'


def query_freebase(query, cursor='', wait=None):
	if wait is None:
		wait = .864

	params = {
		'query': '[{}]'.format(json.dumps(query)),
		'cursor': cursor,
		'key': FREEBASE_API_KEY,
	}

	url = '{}?{}'.format(FREEBASE_API_ENDPOINT, urllib.parse.urlencode(params))

	# With api key I use, I have 100k requests per day limit, which boils down to a bit more than one per second.
	# To avoid forgetting to set this anywhere else, it's here. Better to wait for 1 second than get banned.
	time.sleep(wait)

	request = urllib.request.Request(url)
	try:
		response = urllib.request.urlopen(request)
		return response.read().decode('utf-8')
	except Exception as e:
		logger.error('Error reading from freebase')
		logger.error(e)
		return json.dumps({'error': 'error'})


def clean_date_anomalies(date_string):
	for anomaly, replacement in DATE_ANOMALIES.items():
		date_string = date_string.replace(anomaly, replacement)

	return date_string.strip()


def update_statistical_data(zodiac):
	min_value = min(list(zodiac.get('distributionPercentages').values()))
	max_value = max(list(zodiac.get('distributionPercentages').values()))
	for_update = {
		'min': min_value,
		'max': max_value,
		'range': max_value - min_value,
		'mean': numpy.mean(list(zodiac.get('distributionPercentages').values())),
		'median': numpy.median(list(zodiac.get('distributionPercentages').values())),
		'standardDeviation': numpy.std(list(zodiac.get('distributionPercentages').values())),
		'average': numpy.average(list(zodiac.get('distributionPercentages').values())),
	}

	zodiac.update(for_update)

	return zodiac
