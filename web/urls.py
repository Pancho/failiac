from django.conf.urls import patterns, url


urlpatterns = patterns('web.views',
	# Index
	url(r'^$', 'index', name='web.index'),
)
