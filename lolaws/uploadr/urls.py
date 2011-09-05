from django.conf import settings
from django.conf.urls.defaults import patterns, url

from lolaws.uploadr.views import *

urlpatterns = patterns('',
    url(r'^$', view=upload, name='uploadr-upload'),
    url(r'^success/(?P<image_id>\d+)/', view=success, name='uploadr-success'),
    url(r'^all/$', view=all, name='uploadr-all'),
)

_media_url = settings.MEDIA_URL
if _media_url.startswith('/'):
    _media_url = _media_url[1:]
urlpatterns += patterns('',
    # Serve a favicon, to get rid of those irritating 404 log statements
    (r'^{0}(?P<path>.*)$'.format(_media_url), 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
