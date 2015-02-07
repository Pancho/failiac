import logging
import random
from datetime import datetime


from django.core.management.base import NoArgsCommand
from bson.objectid import ObjectId


from external import zodiac
from external import mongo
from external import utils


logger = logging.getLogger(__name__)

PREPARE_RANDOM_EARTH_POPULATION = True
APPROXIMATE_NUMBER_OF_PEOPLE = 7283810150  # http://www.worldometers.info/world-population/ (will rise)


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		mongo.db.zodiacs.remove()  # First clean
		people_professions = mongo.db.peopleprofessions.find()
		by_length = {}
		counter = 0

		for people_profession in people_professions:
			members = people_profession.get('members')
			profession = people_profession.get('name')
			by_length.setdefault(people_profession.get('length'), []).append({
				'members': members,
				'name': profession,
			})
		logger.info('Professions sorted')

		for length, groups in by_length.items():
			for blob in groups:
				counter += 1

				if length < 12:
				# if length < 100:
				# if length < 366:
					logger.info('Skipping profession {}. Too few members.'.format(blob.get('name')))
					continue

				logger.info('Processing profession {}. Large enough ({}).'.format(blob.get('name'), length))
				object_ids = [ObjectId(member_id) for member_id in blob.get('members')]
				people = mongo.db.people.find({'_id': {'$in': object_ids}})
				distribution = zodiac.get_empty_distribution()

				for person in people:
					sign = zodiac.get_zodiac(person.get('parsedBirthday'))
					distribution[sign] += 1

				mongo.db.zodiacs.insert(utils.update_statistical_data({
					'members': people.count(),
					'distribution': distribution,
					'distributionPercentages': zodiac.convert_to_percentages(distribution),
					'profession': blob.get('name')
				}))

				logger.info('Processed profession {}. {} more to go.'.format(blob.get('name'), people_professions.count() - counter))

		logger.info('Preparing all')
		people_with_parsed_birthday = mongo.db.people.find({'parsedBirthday': {'$exists': True}})
		distribution = zodiac.get_empty_distribution()
		for person in people_with_parsed_birthday:
			sign = zodiac.get_zodiac(person.get('parsedBirthday'))
			distribution[sign] += 1

		mongo.db.zodiacs.insert(utils.update_statistical_data({
			'members': people_with_parsed_birthday.count(),
			'distribution': distribution,
			'distributionPercentages': zodiac.convert_to_percentages(distribution),
			'profession': 'All'
		}))

		logger.info('Copying the prepared normal')
		mongo.db.zodiacs.insert(zodiac.PROBABILITIES_FOR_MONGO)

		if PREPARE_RANDOM_EARTH_POPULATION:
			t0 = datetime.now()
			logger.info('Preparing random Earth population')
			table_signs = list(zodiac.TABLE.values())  # Do not distinct, so we get proper distribution
			distribution = zodiac.get_empty_distribution()

			for i in range(APPROXIMATE_NUMBER_OF_PEOPLE):
				distribution[random.choice(table_signs)] += 1

				if i % 10000000 == 0 and i > 0:
					t1 = datetime.now()
					logger.info('Done {} out of {} ({:.2%}). Time taken so far: {}, estimate till the end: {}'.format(i, APPROXIMATE_NUMBER_OF_PEOPLE, i / APPROXIMATE_NUMBER_OF_PEOPLE, t1 - t0, ((t1 - t0) / (i / APPROXIMATE_NUMBER_OF_PEOPLE))))

			mongo.db.zodiacs.insert(utils.update_statistical_data({
				'members': APPROXIMATE_NUMBER_OF_PEOPLE,
				'distribution': distribution,
				'distributionPercentages': zodiac.convert_to_percentages(distribution),
				'profession': 'Simulated Earth Population'
			}))

			mongo.db.worldpopulation.remove()

			logger.info('Prepared random Earth population')
		else:
			logger.info('Skipping preparation of random Earth population')

		logger.info('Done')
