# -*- coding: utf-8 -*-

# Create your views here.
from django import forms
from django.core import serializers
from django.utils import simplejson
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

from django.http import HttpResponse, HttpResponseBadRequest, \
		HttpResponseNotFound, HttpResponseRedirect

from django.views.generic.base import TemplateView

from dict2xml import dict2xml

import sys
import models
import datautils

#
#
class JSONResponseMixin(object):

	#
	#
	def render_to_response(self, context, **response_kwargs):
		"""
		"""
		response_kwargs['content_type'] = 'application/json'
		return HttpResponse(self.convertContextToJSON(context),
							**response_kwargs)	

	#
	#
	def convertContextToJSON(self, context):
		return simplejson.dumps(context)

#
#
class XMLResponseMixin:

	context_root = None

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
		if self.context_root is None:
			raise ImproperlyConfigured(
                "XMLResponseMixin requires a definition of 'xml_context_root'")

		if isinstance(context, list) or isinstance(context, tuple):
			xmlstr = dict2xml( { self.context_root : context }, 
				self.context_root)
		else:
			xmlstr = dict2xml(context, self.context_root)

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
	context_root = 'components'

	#
	# Overrides get_context_data method from TemplateView
	def get_context_data(self, **kwargs):
		return { 'pagetitle' : 'Components',
				  self.context_root : datautils.getComponentsSummaryAsList()
				}

#
#
class ComponentView(TemplateResponseMixin):
	"""
	Handles the generation of a view for an specific manufacturer
	"""
	template_name = 'component.html'
	context_root = 'component'

	#
	# Overrides the get method from TemplateView
	def get(self, request, *args, **kwargs):
		try:
			context = self.get_context_data(**kwargs)
			return self.render_to_response(context)
		except ObjectDoesNotExist, e:
			return HttpResponseNotFound("Component %s does not exists" %
										kwargs['ref'])

	#
	# Overrides the get_context_data method from TemplateView
	def get_context_data(self, **kwargs):
		ref = kwargs['ref']
		return { 'pagetitle' : ref,
				  self.context_root : datautils.getComponentInfo(ref) }

#
#
class ManufacturersView(TemplateResponseMixin):
	"""
	Handles the generation of the manufacturers view
	"""
	template_name = 'manufacturers.html'
	context_root = 'manufacturers'

	#
	# Overrides the get_context_data method from TemplateView
	def get_context_data(self, **kwargs):
		return { 'pagetitle' : 'Manufacturers',
				  self.context_root : datautils.getManufacturersInfoAsList() }

#
#
class ManufacturerView(TemplateResponseMixin):
	"""
	Handles the generation of a view for an specific manufacturer
	"""
	template_name = 'manufacturer.html'
	context_root = 'manufacturer'

	#
	# Overrides the get method from TemplateView
	def get(self, request, *args, **kwargs):
		try:
			context = self.get_context_data(**kwargs)
			return self.render_to_response(context)
		except ObjectDoesNotExist, e:
			return HttpResponseNotFound("Component %s does not exists" %
										kwargs['name'])

	#
	# Overrides the get_context_data method from TemplateView
	def get_context_data(self, **kwargs):
		name = kwargs['name']
		return { 'pagetitle' : name,
				  self.context_root : datautils.getManufacturerInfo(name) }

#
#
class CategoriesView(TemplateResponseMixin):
	"""
	Handles the generation of the manufacturers view
	"""
	template_name = 'categories.html'
	context_root = 'categories'

	#
	# Overrides the get_context_data method from TemplateView
	def get_context_data(self, **kwargs):
		return { 'pagetitle' : 'Categories',
				  self.context_root : datautils.getCategoriesInfoAsList() }

#
#
class CategoryView(TemplateResponseMixin):
	"""
	Handles the generation of a view for an specific category
	"""
	template_name = 'components.html'
	context_root = 'components'

	#
	# Overrides the get method from TemplateView
	def get(self, request, *args, **kwargs):
		try:
			context = self.get_context_data(**kwargs)
			return self.render_to_response(context)
		except ObjectDoesNotExist, e:
			return HttpResponseNotFound("Component %s does not exists" %
										kwargs['name'])

	#
	# Overrides the get_context_data method from TemplateView
	def get_context_data(self, **kwargs):
		name = kwargs['name']
		return { 'pagetitle' : '[%s] Components' % name,
				  self.context_root : datautils.getCategoryComponentsList(name)}

#
#
class OperatingSystemsView(TemplateResponseMixin):
	"""
	Handles the generation of the operating systems view
	"""
	template_name = 'oss.html'
	context_root = 'oss'

	#
	# Overrides the get_context_data method from TemplateView
	def get_context_data(self, **kwargs):
		return { 'pagetitle' : 'Operating Systems',
				  self.context_root : datautils.getOSsInfoAsList() }


#
#
class OperatingSystemView(TemplateResponseMixin):
	"""
	Handles the generation of a view for an specific operating system
	"""
	template_name = 'os.html'
	context_root = 'os'

	#
	# Overrides the get method from TemplateView
	def get(self, request, *args, **kwargs):
		try:
			context = self.get_context_data(**kwargs)
			return self.render_to_response(context)
		except ObjectDoesNotExist, e:
			return HttpResponseNotFound("Operating system %s does not exists" %
										kwargs['name'])

	#
	# Overrides the get_context_data method from TemplateView
	def get_context_data(self, **kwargs):
		name = kwargs['name']
		return { 'pagetitle' : '[%s] Operating System' % name,
				  self.context_root : datautils.getOSInfo(name)}