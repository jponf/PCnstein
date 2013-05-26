from django.conf.urls import patterns, include, url

from PCnsteinapp.views import MainPageView, ComponentsView, ComponentView, \
                        ManufacturersView, ManufacturerView, CategoriesView, \
                        CategoryView, OperatingSystemsView, OperatingSystemView,\
                        UserView, ComponentCreateView, ComponentModifyView, \
                        ComponentDeleteView, SupportedByView, UserDeleteView, \
                        SupportedByDeleteView, createReview, \
                        registerUser

from PCnsteinapp.serializersviews import ComponentListCreateAPIView, \
                        ComponentUpdateDestroyAPIView, CategoryListAPIView, \
                        CategoryRetrieveAPIView, UserListAPIView, \
                        UserRetrieveAPIView, ManufacturerListAPIView, \
                        ManufacturerRetrieveAPIView, OperatingSystemListAPIView,\
                        OperatingSystemListAPIView, OperatingSystemRetrieveAPIView,\
                        SupportedByListAPIView, SupportedByRetrieveAPIView

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
    url(r'^%s/(?P<pk>[\d])$' % globdata.API_DELETE_USER,
        UserDeleteView.as_view()),

    url(r'^$', MainPageView.as_view()),

    url(r'^%s/$' % globdata.API_COMPONENTS, ComponentsView.as_view()),
    url(r'^%s/(?P<ref>[\w\s\.-]+)/$' % globdata.API_COMPONENTS,
        ComponentView.as_view()),
    
    url(r'^%s/$' % globdata.API_MANUFACTURERS, ManufacturersView.as_view()),
    url( r'^%s/(?P<name>[\w\s\.-]+)/$' % globdata.API_MANUFACTURERS, 
         ManufacturerView.as_view() ),

    url(r'^%s/$' % globdata.API_CATEGORIES, CategoriesView.as_view()),
    url(r'^%s/(?P<name>[\w\s\.&]+)/$' % globdata.API_CATEGORIES,
        CategoryView.as_view()),   

    url(r'^%s/$' % globdata.API_OS, OperatingSystemsView.as_view()),
    url(r'^%s/(?P<name>[\w\s\.]+)/$' % globdata.API_OS,
        OperatingSystemView.as_view()),

    url(r'^%s/$' % globdata.API_USER, UserView.as_view()),

    url(r'^%s/$' % globdata.API_CREATE_COMPONENT,
        ComponentCreateView.as_view()),

    url(r'^%s/(?P<pk>[\w\s\.]+)/$' % globdata.API_MODIFY_COMPONENT,
        ComponentModifyView.as_view()),

    url(r'^%s/(?P<pk>[\w\s\.]+)/$' % globdata.API_DELETE_COMPONENT,
        ComponentDeleteView.as_view()),

    url(r'^%s/(?P<ref>[\w\s\.-]+)$' % globdata.API_CREATE_COMPONENT_REVIEW,
        createReview),

    url(r'^%s/(?P<ref>[\w\s\.-]+)/$' % globdata.API_ADD_SUPPORTEDBY,
        SupportedByView.as_view()),

    url(r'^%s/(?P<pk>[\w\s\.]+)/$' % globdata.API_DELETE_SUPPORTEDBY,
        SupportedByDeleteView.as_view()),
   
)

# Ajax Helpers
urlpatterns += patterns('',
    url(r'^geolocbyip/$', getGeoInformationByIP)
)

# REST API
resturlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/components/$', ComponentListCreateAPIView.as_view(), 
        name='component-list'),
    url(r'^api/components/(?P<pk>[\w\s\.-]+)/$', 
        ComponentUpdateDestroyAPIView.as_view(), name='component-detail'),

    url(r'^api/users/$', UserListAPIView.as_view(), name='user-list'),
    url(r'^api/users/(?P<pk>[\d])/$', UserRetrieveAPIView.as_view(),
        name='user-detail'),

    url(r'^api/categories/$', CategoryListAPIView.as_view(),
        name='category-list'),
    url(r'^api/categories/(?P<pk>[\w\s\.&]+)/$', 
        CategoryRetrieveAPIView.as_view(), name='category-detail'),

    url(r'^api/manufacturers/$', ManufacturerListAPIView.as_view(), 
        name='manufactuer-list'),
    url(r'^api/manufacturers/(?P<pk>[\w\s\.-]+)/$', 
        ManufacturerRetrieveAPIView.as_view(), name='manufacturer-detail'),

    url(r'^api/os/$', OperatingSystemListAPIView.as_view(),
        name='operatingsystem-list'),
    url(r'^api/os/(?P<pk>[\w\s\.]+)/$', OperatingSystemRetrieveAPIView.as_view(),
        name='operatingsystem-detail'),

    url(r'^api/supportedby/$', SupportedByListAPIView.as_view(), 
        name='supportedby-list'),
    url(r'^api/supportedby/(?P<pk>[\d])/$', SupportedByRetrieveAPIView.as_view(),
        name='supportedby-detail')

)

# Format suffixes
resturlpatterns = format_suffix_patterns(resturlpatterns, allowed=['api' ,'json', 'xml'])

urlpatterns += resturlpatterns
