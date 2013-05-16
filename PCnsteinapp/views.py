# -*- coding: utf-8 -*-

from dict2xml import dict2xml
from django.utils import simplejson
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.http import HttpResponse, HttpResponseBadRequest, \
                        HttpResponseNotFound, HttpResponseNotAllowed

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from PCnsteinapp import globdata
import responseutils
import permscheck
import datautils
import urlutils

import models

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

    #
    # Overrides get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        context = super(ComponentsView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'Components'
        context['create_url'] = globdata.API_CREATE_COMPONENT
        context['modify_url'] = globdata.API_MODIFY_COMPONENT
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
                                                ref,
                                                urlutils.getComponentURL(ref))

    #
    # Overrides the get_context_data method from TemplateView
    def get_context_data(self, **kwargs):
        ref = kwargs['ref']
        return { 'pagetitle' : ref,
                  self.context_key : datautils.getComponentInfo(ref) }

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
        context['create_url'] = globdata.API_CREATE_MANUFACTURER
        context['modify_url'] = globdata.API_MODIFY_MANUFACTURER
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
        context['create_url'] = globdata.API_CREATE_CATEGORY
        context['modify_url'] = globdata.API_MODIFY_CATEGORY
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
        context['create_url'] = globdata.API_CREATE_OS
        context['modify_url'] = globdata.API_MODIFY_OS
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
class CreateViewGroupRestriction(CreateView):

    groups=None

    def form_valid(self, form):
        if self.groups is None:
            raise ImproperlyConfigured(
                "CreateViewGroupRestriction requires 'groups' to be a list of "
                "group names")

        for g in self.groups:
            if not permscheck.isUserInGroup(self.request.user, g):
                reason = 'User must be member of group: %s' % g
                return responseutils.getHttpResponseForbiddenHTML(
                    'Creation forbidden', reason)

        return super(CreateViewGroupRestriction, self).form_valid(form)     

#
#
class UpdateViewGroupRestriction(UpdateView):

    groups=None

    def form_valid(self, form):
        if self.groups is None:
            raise ImproperlyConfigured(
                "UpdateViewGroupRestriction requires 'groups' to be a list of "
                "group names")

        for g in self.groups:
            if not permscheck.isUserInGroup(self.request.user, g):
                reason = 'User must be member of group: %s' % g
                return responseutils.getHttpResponseForbiddenHTML(
                    'Creation forbidden', reason)

        return super(UpdateViewGroupRestriction, self).form_valid(form) 
#
#
class ManufacturerCreateView(CreateViewGroupRestriction):
    template_name = 'create.html'
    model = models.Manufacturer
    success_url = '/%s' % globdata.API_MANUFACTURERS
    groups = ['Vendor']

#
#
class ComponentCreateView(CreateViewGroupRestriction):
    template_name = 'create.html'
    model = models.Component
    success_url = '/%s' % globdata.API_COMPONENTS
    groups = ['Vendor']

#
#
class CategoryCreateView(CreateViewGroupRestriction):
    template_name = 'create.html'
    model = models.Category
    success_url = '/%s' % globdata.API_CATEGORIES
    groups = ['Vendor']

#
#
class OSCreateView(CreateViewGroupRestriction):
    template_name = 'create.html'
    model = models.OperatingSystem
    success_url = '/%s' % globdata.API_OS
    groups = ['Vendor']

#
#
class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = models.Manufacturer
        exclude = 'name'

#
#
class ManufacturerModifyView(UpdateViewGroupRestriction):
    template_name = 'modify.html'
    model = models.Manufacturer
    form_class = ManufacturerForm  
    success_url = '/%s' % globdata.API_MANUFACTURERS
    groups = ['Vendor']

#
#
class ComponentForm(forms.ModelForm):
    class Meta:
        model = models.Component
        exclude = 'ref'

#
#
class ComponentModifyView(UpdateViewGroupRestriction):
    template_name = 'modify.html'
    model = models.Component
    form_class = ComponentForm  
    success_url = '/%s' % globdata.API_COMPONENTS
    groups = ['Vendor']

#
#
class CategoryModifyView(UpdateViewGroupRestriction):
    template_name = 'modify.html'
    model = models.Category 
    success_url = '/%s' % globdata.API_CATEGORIES
    groups = ['Vendor']

#
#
class OSModifyView(UpdateViewGroupRestriction):
    template_name = 'modify.html'
    model = models.OperatingSystem
    success_url = '/%s' % globdata.API_OS
    groups = ['Vendor']

#
#
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'