import logging
import json
import re
from datetime import datetime


from django.core.management.base import NoArgsCommand


from external import mongo
from external import utils


logger = logging.getLogger(__name__)
birthday_pattern = re.compile(r'Date of birth')


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		limit = 100
		counter = 0
		all_people_count = mongo.db.people.find({'birthdayProcessed': {'$exists': False}}).count()
		failed = set()

		while True:
			people = mongo.db.people.find({'birthdayProcessed': {'$exists': False}})[:limit]
			result_length = people.count(with_limit_and_skip=True)

			for person in people:
				counter += 1

				birthday = person.get('birthday')
				parsed_date = None

				if birthday is not None:
					birthday = utils.clean_date_anomalies(birthday)

				for date_format in utils.DATE_FORMATS:
					try:
						parsed_date = datetime.strptime(birthday, date_format)
						break
					except:
						pass  # Just try again

				if parsed_date is None:
					failed.add(birthday)
				else:
					person['parsedBirthday'] = parsed_date

				# Due to large amount of data, for a PC, I rather mark the seen records, so I can interrupt and
				# rerun at any time.
				person['birthdayProcessed'] = True
				mongo.upsert_blob(mongo.db.people, person, 'freebaseId')

			if result_length != limit:
				break

			logger.info('Done {} out of {}, result length was {}'.format(counter, all_people_count, result_length))

		logger.info('Failed: {} ({:.2%} of all - {})'.format(len(failed), len(failed) / all_people_count, all_people_count))
		# Store failed attempts at parsing so you can see later if there are any mangled dates that can be salvaged
		file = open('external/fixtures/faileddates.json', 'w')
		file.write(json.dumps(list(failed), indent=4))
		file.close()
