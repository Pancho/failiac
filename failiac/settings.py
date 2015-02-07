import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)


SECRET_KEY = 'Your Django secret here'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'external',
	'web',
)
MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'failiac.urls'
WSGI_APPLICATION = 'failiac.wsgi.application'
# Usually don't need this if using pymongo, but since I'm not using auth at all, and all the hacks that come with it,
# I need to declare this.
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': here('../failiac.db'),
		'TEST_NAME': here('../test_failiac.db'),
		'USER': '',
		'PASSWORD': '',
		'HOST': '',
		'PORT': '',
	}
}
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'standard': {
			'format': '%(asctime)s [%(levelname)s] (%(module)s:%(lineno)d): %(message)s'
		},
	},
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'standard'
		},
		'default_file': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': here('../logs/www.log'),
			'maxBytes': 1024 * 1024 * 100, # 100 MB
			'backupCount': 10,
			'formatter': 'standard',
		},
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
		'external': {
			'handlers': ['console', 'default_file'],
			'level': 'DEBUG',
			'propagate': True,
		},
		'web': {
			'handlers': ['console', 'default_file'],
			'level': 'DEBUG',
			'propagate': True,
		},
	}
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = ''
STATIC_URL = '/media/admin/'
APPEND_SLASH = False
MONGO_DB_ENDPOINT_URL = 'localhost'
MONGO_DB_ENDPOINT_PORT = 27017
MONGODB_DB_NAME = 'failiac'  # Do change this
