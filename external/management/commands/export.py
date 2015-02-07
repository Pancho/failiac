import logging
import json


from django.core.management.base import NoArgsCommand
from bson import json_util


from external import mongo


logger = logging.getLogger(__name__)


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		zodiacs = list(mongo.db.zodiacs.find())

		file = open('external/fixtures/zodiacs.json', 'w')
		file.write(json.dumps(list(zodiacs), indent=4, default=json_util.default))
		file.close()
