import logging
import json
import os


from django.core.management.base import NoArgsCommand
from django.template import Context, Template


from external import encoders
from external import mongo
from external import zodiac


logger = logging.getLogger(__name__)


TEMPLATE = '''FailiacZodiacs = {{ dump|safe }}
FailiacZodiacs.getSign = function (date) {if (date.getDate() === 29 && date.getMonth() === 1) { return \'Pisces\';} return FailiacZodiacs.signs[date.getDate() + \',\' + (date.getMonth() + 1)];}
'''
OMIT_PROFESSIONS_IN_NAMES = ['All', 'Birthed', 'Simulated Earth Population', '/m/02h65y5', None]


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../media/')
		zodiacs = {}
		zodiacs_list = []

		for zodiac_blob in mongo.db.zodiacs.find():
			zodiacs[zodiac_blob.get('profession')] = zodiac_blob
			zodiacs_list.append(zodiac_blob)

		names = list(zodiacs.keys())
		for omitted in OMIT_PROFESSIONS_IN_NAMES:
			if omitted in names:
				names.remove(omitted)

		by_members = []
		for profession in [blob.get('profession') for blob in sorted(zodiacs_list, key=lambda blob: blob['members'])]:
			if profession not in OMIT_PROFESSIONS_IN_NAMES:
				by_members.append(profession)

		by_standard_deviation = []
		for profession in [blob.get('profession') for blob in sorted(zodiacs_list, key=lambda blob: blob['standardDeviation'])]:
			if profession not in OMIT_PROFESSIONS_IN_NAMES:
				by_standard_deviation.append(profession)

		by_range = []
		for profession in [blob.get('profession') for blob in sorted(zodiacs_list, key=lambda blob: blob['range'])]:
			if profession not in OMIT_PROFESSIONS_IN_NAMES:
				by_range.append(profession)

		ctx = {
			'names': sorted(names),
			'byMembers': by_members,
			'byStandardDeviation': by_standard_deviation,
			'byRange': by_range,
			'zodiacs': zodiacs,
			'signs': zodiac.TABLE_AS_JSON,
			'order': zodiac.ORDER,
		}

		file_path = '{}js/zodiacs.js'.format(root)
		if os.path.isfile(file_path):
			os.remove(file_path)

		js_file = open(file_path, 'w')

		template = Template(TEMPLATE)
		ctx = Context({
			'dump': json.dumps(ctx, cls=encoders.VersatileJSONEncoder, indent=4),
		})

		js_file.write(template.render(ctx))
		js_file.close()


