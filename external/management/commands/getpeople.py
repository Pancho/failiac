import logging
import json
from datetime import datetime


from django.core.management.base import NoArgsCommand


from external import utils
from external import mongo


logger = logging.getLogger(__name__)


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		cursor = ''
		retries = 0

		t0 = datetime.now()

		while True:
			t00 = datetime.now()
			blob = json.loads(utils.query_freebase({
				'id': None,
				'type': '/people/person',
				'name': None,
				'/people/person/date_of_birth': None,
				'/people/person/gender': None,
				'/people/person/religion': [],
				'/people/person/nationality': [],
				'/people/person/profession': []
			}, cursor))

			if 'error' in blob:  # Retry
				retries += 1
				logger.warn('Retrying query ({}), cursor: {}'.format(retries, cursor))
				continue

			retries = 0

			cursor = blob.get('cursor')
			blob_result = blob.get('result')

			for result in blob_result:
				# Clean the resultset
				result['professions'] = result.get('/people/person/profession')
				del result['/people/person/profession']
				result['birthday'] = result.get('/people/person/date_of_birth')
				del result['/people/person/date_of_birth']
				result['gender'] = result.get('/people/person/gender')
				del result['/people/person/gender']
				result['nationality'] = result.get('/people/person/nationality')
				del result['/people/person/nationality']
				result['religion'] = result.get('/people/person/religion')
				del result['/people/person/religion']
				result['freebaseId'] = result.get('id')
				del result['id']
				# Save
				mongo.db.people.insert(result)

			t01 = datetime.now()
			logger.info('Fetching more, so far {}, took {} so far / {} for this iteration.'.format(mongo.db.people.count(), t01 - t0, t01 - t00))

			if not cursor:
				break
