import logging
import json


from django.core.management.base import NoArgsCommand


from external import utils
from external import mongo


logger = logging.getLogger(__name__)


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		mongo.db.professions.remove()  # Clean the DB first
		result = []
		cursor = ''

		while True:
			blob = json.loads(utils.query_freebase({'name': None, 'type': '/people/profession'}, cursor))
			cursor = blob.get('cursor')
			blob_result = blob.get('result')
			result.extend(blob_result)

			if not cursor:
				break

			logger.info('Fetching more, so far {}'.format(len(result)))

		professions = {
			profession.get('name'): profession.get('type') for profession in result
		}

		logger.info('Eliminated {} duplicates'.format(len(result) - len(list(professions.keys()))))

		for name, profession_type in professions.items():
			mongo.db.professions.insert({
				'name': name,
				'type': profession_type,
			})
