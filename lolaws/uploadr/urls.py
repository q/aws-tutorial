from django.conf.urls.defaults import patterns, url
from lolaws.uploadr.views import *

urlpatterns = patterns('',
    url(r'^$', view=upload, name='uploadr-upload'),
    url(r'^success/(?P<image_id>\d+)/', view=success, name='uploadr-success'),
    url(r'^all/$', view=all, name='uploadr-all'),
)
