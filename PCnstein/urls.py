from django.conf.urls import patterns, include, url

from PCnsteinapp.views import MainPageView, ComponentsView, ComponentView, \
                        ManufacturersView, ManufacturerView, CategoriesView, \
                        CategoryView, OperatingSystemsView, OperatingSystemView,\
                        ManufacturerCreateView, ComponentCreateView, \
                        UserCreateView

from PCnsteinapp import globdata

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
    url(r'^register/$', UserCreateView.as_view() ),

    url(r'^$', MainPageView.as_view()),

    url(r'^%s/$' % globdata.API_COMPONENTS, ComponentsView.as_view()),
    url(r'^%s/(?P<ref>[\w\s]+)/$' % globdata.API_COMPONENTS,
        ComponentView.as_view()),
    
    url(r'^%s/$' % globdata.API_MANUFACTURERS, ManufacturersView.as_view()),
    url( r'^%s/(?P<name>[\w\s]+)/$' % globdata.API_MANUFACTURERS, 
         ManufacturerView.as_view() ),

    url(r'^%s/$' % globdata.API_CATEGORIES, CategoriesView.as_view()),
    url(r'^%s/(?P<name>[\w\s]+)/$' % globdata.API_CATEGORIES,
        CategoryView.as_view()),   

    url(r'^%s/$' % globdata.API_OS, OperatingSystemsView.as_view()),
    url(r'^%s/(?P<name>[\w\s]+)/$' % globdata.API_OS,
        OperatingSystemView.as_view()),

    url(r'^%s/$' % globdata.API_CREATE_MANUFACTURER,
        ManufacturerCreateView.as_view()),

    url(r'^%s/$' % globdata.API_CREATE_COMPONENT,
        ComponentCreateView.as_view())
)