import logging
import os
import shutil


from django.core.management.base import NoArgsCommand


logger = logging.getLogger(__name__)


FILES = {
	'media/js/zodiacs.js': 'export/zodiacs.js',
	'media/js/jquery.js': 'export/jquery.js',
	'media/js/failiac.js': 'export/failiac.js',
	'media/css/reset.css': 'export/reset.css',
	'media/css/default.css': 'export/default.css',
	'media/css/font-awesome.css': 'export/font-awesome.css',
	'media/fonts/fontawesome-webfont.eot': 'export/fonts/fontawesome-webfont.eot',
	'media/fonts/fontawesome-webfont.svg': 'export/fonts/fontawesome-webfont.svg',
	'media/fonts/fontawesome-webfont.ttf': 'export/fonts/fontawesome-webfont.ttf',
	'media/fonts/fontawesome-webfont.woff': 'export/fonts/fontawesome-webfont.woff',
	'web/templates/index.html': 'export/index.html',
}

REPLACEMENTS = {
	'export/font-awesome.css': [
		{
			'chunk': '../fonts/',
			'replacement': 'fonts/',
		},
	],
	'export/index.html': [
		{
			'chunk': '/media/js/',
			'replacement': '',
		},
		{
			'chunk': '/media/css/',
			'replacement': '',
		},
	],
}

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		# Reset folder
		if os.path.exists('export'):
			shutil.rmtree('export')
		os.mkdir('export')
		os.mkdir('export/fonts')

		for source, destination in FILES.items():
			shutil.copy(source, destination)

		for path, rules in REPLACEMENTS.items():
			file = open(path, 'r')
			contents = file.read()
			file.close()

			for rule in rules:
				chunk = rule.get('chunk')
				replacement = rule.get('replacement')

				contents = contents.replace(chunk, replacement)

			file = open(path, 'w')
			file.write(contents)
			file.close()

