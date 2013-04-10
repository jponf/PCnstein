from django.conf.urls import patterns, include, url

from PCnsteinapp.views import GetComponents, GetComponent, GetMainPage, \
                            GetManufacturers, GetManufacturer, GetCategories, \
                            GetCategory, GetOSes, GetOS, RegisterUser

from PCnsteinapp.globdata import API_MANUFACTURERS, API_COMPONENTS, \
                            API_CATEGORIES, API_OS

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PCnstein.views.home', name='home'),
    # url(r'^PCnstein/', include('PCnstein.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                     { 'next_page' : '/'}),
    url(r'^register/$', RegisterUser),

    url(r'^$', GetMainPage),

    url(r'^%s/$' % API_COMPONENTS, GetComponents),
    url(r'^%s/([\w\s]+)/$' % API_COMPONENTS, GetComponent), # \w only matches alphanumerical chars and underscores. If all but blanks wanted change it for \S.
    
    url(r'^%s/$' % API_MANUFACTURERS, GetManufacturers),
    url(r'^%s/([\w\s]+)/$' % API_MANUFACTURERS, GetManufacturer),

    url(r'^%s/$' % API_CATEGORIES, GetCategories),
    url(r'^%s/([\w\s]+)/$' % API_CATEGORIES, GetCategory),   

    url(r'^%s/$' % API_OS, GetOSes),
    url(r'^%s/([\w\s]+)/$' % API_OS, GetOS),
)
