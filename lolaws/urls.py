from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib import admin

admin.autodiscover()

handler404 = 'lolaws.core.views.server_error'
handler500 = 'lolaws.core.views.server_error'

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url':'/uploadr/'}),
    url(r'^uploadr/', include('lolaws.uploadr.urls')),
    #url(r'^lolaws/', include('lolaws.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
