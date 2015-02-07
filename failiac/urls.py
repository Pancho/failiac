from django.conf.urls import patterns, include, url


from failiac import settings


urlpatterns = patterns('',
	# WEB
	(r'', include('web.urls')),

	# STATIC CONTENT
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)