from django.conf.urls import patterns, include, url

from PCnsteinapp.views import MainPageView, ComponentsView, ComponentView, \
                        ManufacturersView, ManufacturerView, CategoriesView, \
                        CategoryView, OperatingSystemsView, OperatingSystemView,\
                        ComponentCreateView, ComponentModifyView, ComponentDeleteView,\
                        createReview, registerUser

from PCnsteinapp.serializersviews import ComponentCreateAPIView, \
                        ComponentUpdateDestroyAPIView

from PCnsteinapp.ajaxhelper import getGeoInformationByIP

from PCnsteinapp import globdata

from rest_framework.urlpatterns import format_suffix_patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
##################################################

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

    url(r'^register/$', registerUser ),

    url(r'^$', MainPageView.as_view()),

    url(r'^%s/$' % globdata.API_COMPONENTS, ComponentsView.as_view()),
    url(r'^%s/(?P<ref>[\w\s\.]+)/$' % globdata.API_COMPONENTS,
        ComponentView.as_view()),
    
    url(r'^%s/$' % globdata.API_MANUFACTURERS, ManufacturersView.as_view()),
    url( r'^%s/(?P<name>[\w\s\.]+)/$' % globdata.API_MANUFACTURERS, 
         ManufacturerView.as_view() ),

    url(r'^%s/$' % globdata.API_CATEGORIES, CategoriesView.as_view()),
    url(r'^%s/(?P<name>[\w\s\.]+)/$' % globdata.API_CATEGORIES,
        CategoryView.as_view()),   

    url(r'^%s/$' % globdata.API_OS, OperatingSystemsView.as_view()),
    url(r'^%s/(?P<name>[\w\s\.]+)/$' % globdata.API_OS,
        OperatingSystemView.as_view()),

    url(r'^%s/$' % globdata.API_CREATE_COMPONENT,
        ComponentCreateView),

    url(r'^%s/(?P<pk>[\w\s\.]+)/$' % globdata.API_MODIFY_COMPONENT,
        ComponentModifyView.as_view()),

    url(r'^%s/(?P<pk>[\w\s\.]+)/$' % globdata.API_DELETE_COMPONENT,
        ComponentDeleteView.as_view()),

    url(r'^%s/(?P<ref>[\w\s\.]+)$' % globdata.API_CREATE_COMPONENT_REVIEW,
        createReview)
   
)

# Ajax Helpers
urlpatterns += patterns('',
    url(r'^geolocbyip/$', getGeoInformationByIP)
)

# REST API
resturlpatterns = patterns('',
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    url(r'^api/components/$', ComponentCreateAPIView.as_view(), name='component-list'),
    url(r'^api/components/(?P<pk>[\w\s\.]+)/$', 
        ComponentUpdateDestroyAPIView.as_view(), name='component-detail'),
)

# Format suffixes
resturlpatterns = format_suffix_patterns(resturlpatterns, allowed=['api' ,'json', 'xml'])

urlpatterns += resturlpatterns
