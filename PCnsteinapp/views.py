# -*- coding: utf-8 -*-

from dict2xml import dict2xml
from django.utils import simplejson
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.http import HttpResponse, HttpResponseBadRequest, \
                        HttpResponseRedirect, Http404

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.middleware import csrf

from PCnsteinapp import globdata
import responseutils
import permscheck
import datautils
import urlutils
import models
import forms

#
#
class JSONResponseMixin(object):

    # Used to identify and separate the data context and ignore html context
    context_key = None

    #
    #
    def render_to_response(self, context, **response_kwargs):
        """
        Generates a response in JSON with the given context
        """
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(self.convertContextToJSON(context),
                            **response_kwargs)  

    #
    #
    def convertContextToJSON(self, context):
        # Extract important data
        context = context[self.context_key]
        return simplejson.dumps(context)

#
#
class XMLResponseMixin:

    # Used to identify and separate the data context and ignore html context
    context_key = None

    #
    #
    def render_to_response(self, context, **response_kwargs):
        """
        Generates a response in XML with the given context
        """
        response_kwargs['content_type'] = 'application/xml'
        return HttpResponse(self.convertToXML(context),
                            **response_kwargs)
    
    #
    #
    def convertToXML(self, context):
        """
        Returns the xml representation of the given data
        """

        # Extract important data
        context = context[self.context_key]

        if self.context_key is None:
            raise ImproperlyConfigured(
                "XMLResponseMixin requires a definition of 'xml_context_key'")

        if isinstance(context, list) or isinstance(context, tuple):
            xmlstr = dict2xml( { self.context_key : context }, 
                self.context_key)
        else:
            xmlstr = dict2xml(context, self.context_key)

        return xmlstr

#
#
class TemplateResponseMixin(TemplateView, XMLResponseMixin, JSONResponseMixin):

    #
    #
    def render_to_response(self, context):
        format = self.request.GET.get('format', 'html')

        if format.lower() == 'json':
            return JSONResponseMixin.render_to_response(self, context)
        elif format.lower() == 'xml':
            return XMLResponseMixin.render_to_response(self, context)
        elif format.lower() == 'html':
            return TemplateView.render_to_response(self, context)
        else:
            return HttpResponseBadRequest()

#
#
class MainPageView(TemplateView):
    """
    Handles he generation of the main page
    """
    template_name = 'mainpage.html'

    def get_context_data(self, **kwargs):
        """
        Return the context used to generate the main page
        """
        return { 'user' : self.request.user }


#
#
class ComponentsView(TemplateResponseMixin):
    """
    Handles the generatioin of the components view
    """
    template_name = 'components.html'
    context_key = 'components'
    permitted = ['Vendor']

    #
    # Overrides get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        context = super(ComponentsView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'Components'
        context['create_url'] = urlutils.getCreateComponentURL()
        context['can_create'] = False 
        for g in self.permitted:
            if permscheck.isUserInGroup(self.request.user, g):
                context['can_create'] = True
                break

        context[self.context_key] = datautils.getComponentsSummaryAsList()
        return context

#
#
class ComponentView(TemplateResponseMixin):
    """
    Handles the generation of a view for an specific manufacturer
    """
    template_name = 'component.html'
    context_key = 'component'

    #
    # Overrides the get method from TemplateView
    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

        except ObjectDoesNotExist:
            ref = kwargs['ref']
            return responseutils.getHttpResponseNotFoundHTML(
                                                '%s Not Found' % ref,
                                                request.user,
                                                ref,
                                                urlutils.getComponentURL(ref))

    #
    # Overrides the get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        ref = kwargs['ref']
        cinfo = datautils.getComponentInfo(ref)

        context = super(ComponentView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'Components'
        context['modify_url'] = urlutils.getModifyComponentURL(ref)
        context['delete_url'] = urlutils.getDeleteComponentURL(ref)
        context['add_supportedby_url'] = urlutils.getAddSupportedByURL(ref)
        context['is_creator'] = cinfo['createdby'] == str(self.request.user)
        context['RATING_CHOICES'] = models.Review.RATING_CHOICES
        context['create_review_url'] = urlutils.getCreateComponentReviewURL(ref)
        context[self.context_key] = cinfo
        
        return context

#
#
class ManufacturersView(TemplateResponseMixin):
    """
    Handles the generation of the manufacturers view
    """
    template_name = 'manufacturers.html'
    context_key = 'manufacturers'

    #
    # Overrides the get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        context = super(ManufacturersView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'Manufacturers'
        context[self.context_key] = datautils.getManufacturersInfoAsList()
        return context

#
#
class ManufacturerView(TemplateResponseMixin):
    """
    Handles the generation of a view for an specific manufacturer
    """
    template_name = 'manufacturer.html'
    context_key = 'manufacturer'

    #
    # Overrides the get method from TemplateView
    def get(self, request, *args, **kwargs):
        try: 
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        except ObjectDoesNotExist:
            name = kwargs['name']
            return responseutils.getHttpResponseNotFoundHTML(
                                            '%s Not Found' % name,
                                            request.user,
                                            name,
                                            urlutils.getManufacturerURL(name))

    #
    # Overrides the get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        name = kwargs['name']
        return { 'pagetitle' : name,
                  self.context_key : datautils.getManufacturerInfo(name) }

#
#
class CategoriesView(TemplateResponseMixin):
    """
    Handles the generation of the manufacturers view
    """
    template_name = 'categories.html'
    context_key = 'categories'

    #
    # Overrides the get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        context = super(CategoriesView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'Categories'
        context[self.context_key] = datautils.getCategoriesInfoAsList()
        return context

#
#
class CategoryView(TemplateResponseMixin):
    """
    Handles the generation of a view for an specific category
    """
    template_name = 'components.html'
    context_key = 'components'

    #
    # Overrides the get method from TemplateView
    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        except ObjectDoesNotExist, e:
            name = kwargs['name']
            return responseutils.getHttpResponseNotFoundHTML(
                                            '%s Not Found' % name,
                                            request.user,
                                            name,
                                            urlutils.getCategoryURL(name))

    #
    # Overrides the get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        name = kwargs['name']
        return { 'pagetitle' : '[%s] Components' % name,
                  self.context_key : datautils.getCategoryComponentsList(name)}

#
#
class OperatingSystemsView(TemplateResponseMixin):
    """
    Handles the generation of the operating systems view
    """
    template_name = 'oss.html'
    context_key = 'oss'

    #
    # Overrides the get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        context = super(OperatingSystemsView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'Operating systems'
        context[self.context_key] = datautils.getOSsInfoAsList()
        return context


#
#
class OperatingSystemView(TemplateResponseMixin):
    """
    Handles the generation of a view for an specific operating system
    """
    template_name = 'os.html'
    context_key = 'os'

    #
    # Overrides the get method from TemplateView
    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        except ObjectDoesNotExist, e:
            name = kwargs['name']
            return responseutils.getHttpResponseNotFoundHTML(
                                        '%s Not Found' % name,
                                        request.user,
                                        name,
                                        urlutils.getOperatingSystemURL(name))

    #
    # Overrides the get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        name = kwargs['name']
        return { 'pagetitle' : '[%s] Operating System' % name,
                  self.context_key : datautils.getOSInfo(name)}

#
#
class UserView(TemplateResponseMixin):
    """
    Handles the generation of a view for an specific user
    """
    template_name = 'userprofile.html'
    context_key = 'userprofile'

    #
    # Overrides the get method from TemplateView
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            reason = "User must be logged in to see a user profile"
            return responseutils.getHttpResponseBadRequestHTML(
                                        'User Not Logged',
                                        request.user,
                                        reason)

    #
    # Overrides the get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        uinfo = datautils.getLoggedUserInfo(self.request.user)

        context['pagetitle'] = '%s Profile' % uinfo['username']
        context['delete_url'] = urlutils.getDeleteUserURL(uinfo['id'])
        context[self.context_key] = uinfo

        return context

#
#
class CreateViewGroupRestriction(CreateView):

    groups=None

    def dispatch(self, *args, **kwargs):
        self.kargs = kwargs
        self.args = args

        return super(CreateViewGroupRestriction, self).dispatch(*args, **kwargs) 

    def form_valid(self, form):
        print 'Group Restriction'
        if self.groups is None:
            raise ImproperlyConfigured(
                "CreateViewGroupRestriction requires 'groups' to be a list of "
                "group names")

        if not self.request.user.is_authenticated():
            reason = 'User must be logged in'
            return responseutils.getHttpResponseForbiddenHTML(
                'Creation forbidden', self.request.user, reason)

        for g in self.groups:
            if not permscheck.isUserInGroup(self.request.user, g):
                reason = 'User must be member of group: %s' % g
                return responseutils.getHttpResponseForbiddenHTML(
                    'Creation forbidden', self.request.user, reason)

        return super(CreateViewGroupRestriction, self).form_valid(form)     

#
#
class UpdateViewGroupRestriction(UpdateView):

    groups=None

    def dispatch(self, *args, **kwargs):
        self.kargs = kwargs
        self.args = args

        return super(CreateViewGroupRestriction, self).dispatch(*args, **kwargs) 

    def form_valid(self, form):
        if self.groups is None:
            raise ImproperlyConfigured(
                "UpdateViewGroupRestriction requires 'groups' to be a list of "
                "group names")

        if not self.request.user.is_authenticated():
            reason = 'User must be logged in'
            return responseutils.getHttpResponseForbiddenHTML(
                'Update forbidden', self.request.user, reason)

        for g in self.groups:
            if not permscheck.isUserInGroup(self.request.user, g):
                reason = 'User must be member of group: %s' % g
                return responseutils.getHttpResponseForbiddenHTML(
                    'Update forbidden', self.request.user, reason)

        return super(UpdateViewGroupRestriction, self).form_valid(form) 

#
#
class ComponentCreateView(CreateViewGroupRestriction):
    template_name = 'create.html'
    model = models.Component
    form_class = forms.CreateComponentForm
    success_url = '/%s' % globdata.API_COMPONENTS
    groups = ['Vendor']

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.createdby = self.request.user
        return super(ComponentCreateView, self).form_valid(form)


#
#
class SupportedByView(CreateViewGroupRestriction):
    template_name = 'create.html'
    model = models.SupportedBy
    form_class = forms.SupportedByForm
    groups = ['Vendor']

    def get_success_url(self):
        return urlutils.getComponentURL(self.kwargs['ref'])

    def form_valid(self, form):
        comp = models.Component.objects.get(pk=self.kwargs['ref'])

        if not self.request.user == comp.createdby:
            reason = 'Only the One and Only Creator can modify his spawn'
            return responseutils.getHttpResponseForbiddenHTML(
                    'Creation forbidden', self.request.user, reason)

        form.instance.component = comp
        return super(SupportedByView, self).form_valid(form)

#
# 
class ComponentModifyView(UpdateViewGroupRestriction):
    template_name = 'modify.html'
    model = models.Component
    form_class = forms.ModifyComponentForm  
    success_url = '/%s' % globdata.API_COMPONENTS
    groups = ['Vendor']

#
#
class ComponentDeleteView(DeleteView):
    template_name = 'delete_confirmation.html'
    model = models.Component
    success_url = '/%s' % globdata.API_COMPONENTS

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()

        if not self.object.createdby == self.request.user:
            reason = 'User must be the create of the component to delete it'
            return responseutils.getHttpResponseForbiddenHTML(
                'Component Deletion forbidden', self.request.user, reason)

        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

#
#
class SupportedByDeleteView(DeleteView):
    template_name = 'delete_confirmation.html'
    model = models.SupportedBy
    success_url = '/%s' % globdata.API_COMPONENTS

    def get_success_url(self):
        return urlutils.getComponentURL(self.object.component.ref)

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()

        if not self.object.component.createdby == self.request.user:
            reason = 'User must be the creator of the relation to delete it'
            return responseutils.getHttpResponseForbiddenHTML(
                'Supported By Deletion forbidden', self.request.user, reason)

        # In order to get the correct URL the order is important
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

#
#
class UserDeleteView(DeleteView):
    template_name = 'delete_confirmation.html'
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        authuser = self.request.user
        self.object = self.get_object()

        if authuser.is_authenticated():
            if not authuser == self.object:
                reason = 'You are not allowed to delete other users'
                return responseutils.getHttpResponseForbiddenHTML(
                    'User Deletion forbidden', self.request.user, reason)
            logout(request)
        else:
            reason = 'You must be logged in to delete your user'
            return responseutils.getHttpResponseForbiddenHTML(
                'User Deletion forbidden', self.request.user, reason)

        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


#
# TEMPORAL
#
def createReview(request, ref):
    
    try:
        datautils.createComponentReview(ref, 
                                    request.user,
                                    request.POST['rating'],
                                    request.POST['comment'])

        return HttpResponseRedirect(urlutils.getComponentURL(ref))
    except ObjectDoesNotExist:    
        return responseutils.getHttpResponseNotFoundHTML('%s Not Found' % ref,
                                                request.user,
                                                ref,
                                                urlutils.getComponentURL(ref))

#
#
def registerUser(request):

    if request.method == 'POST':

        uf = UserCreationForm(request.POST, prefix='user')
        upf = forms.UserProfileForm(request.POST, prefix='userprofile')

        if uf.is_valid() and upf.is_valid():
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.user = user
            userprofile.save()

            # Get form user data to automatically authenticate it
            authuser = authenticate(username = request.POST['user-username'],
                                    password = request.POST['user-password1'])
            login(request, authuser)
            return HttpResponseRedirect(urlutils.getUserURL())
            
        else:
            context = {
                'pagetitle' : 'New User Registration',
                'userform' : uf,
                'userprofileform' : upf,
                'csrf_token' : csrf.get_token(request)
            }
            response_str = render_to_string('registration/register.html', context)
            return HttpResponse(response_str, content_type='text/html')

    elif request.method == 'GET':

        uf = UserCreationForm(prefix='user')
        upf = forms.UserProfileForm(prefix='userprofile')
        context = {
            'pagetitle' : 'New User Registration',
            'userform' : uf,
            'userprofileform' : upf,
            'csrf_token' : csrf.get_token(request)
        }

        response_str = render_to_string('registration/register.html', context)
        return HttpResponse(response_str, content_type='text/html')

    else:
        return responseutils.getHttpResponseNotFoundHTML('WTF', request.user, 
                                                        'YOU', 'JERK')
