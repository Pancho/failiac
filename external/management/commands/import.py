import logging
import json


from django.core.management.base import NoArgsCommand
from bson import json_util


from external import mongo


logger = logging.getLogger(__name__)


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		file = open('external/fixtures/zodiacs.json', 'r')
		zodiacs = json.loads(file.read(), object_hook=json_util.object_hook)
		file.close()

		if len(zodiacs) > 0:
			mongo.db.zodiacs.remove()
			mongo.db.zodiacs.insert(zodiacs)
