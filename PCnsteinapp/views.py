# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.core import serializers
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

from dict2xml import dict2xml

import sys
import models
import datautils

#
#
def GetMainPage(request):
	"""
	GetMainPage(request) -> HttpResponse
	Returns the main page of the application (only html)
	"""
	return render_to_response('mainpage.html')

#
#
def GenerateResponse(request, data, root=None, xmltemplate=None,
					htmltemplate=None):
	"""
	TODO
	"""
	response = None
	format = request.GET.get('format', 'html')

	if format == 'json':
		response = HttpResponse(simplejson.dumps(data),
								mimetype='application/json')		

	elif format == 'xml':
		if not root:
			raise Exception("root must be specified to generate an xml response")

		xmlstr = ''
		if xmltemplate:
			xmlstr = render_to_string(xmltemplate, { root : data } )
		else:
			if isinstance(data, list) or isinstance(data, tuple):
				xmlstr = dict2xml( { root : data }, root )
			else:
				xmlstr = dict2xml(data, root)

		response = HttpResponse(xmlstr, mimetype='application/xml')

	elif format == 'html':
		if not htmltemplate:
			raise Exception("htmltemplate must be specified to generate an "
				"html response")

		response = render_to_response(htmltemplate, data)
	else:
		response = HttpResponseBadRequest(
			'Wrong parameter "format" [html, xml, json]')

	return response


#
#
def GetComponents(request):
	"""
	GetComponents(request) -> HttpResponse
	Returns a list with all the components in the specified format
	"""
	return GenerateResponse(request,
					datautils.GetComponentsSummaryAsList(),
					'components',
					None,
					'components.html')		

#
#
def GetComponent(request, ref):
	"""
	GetComponent(request) -> HttpResponse
	Returns a list with all the information of the specified component
	"""
	try:
		return GenerateResponse(request,
			datautils.GetComponentInfo(ref),
			'component',
			None,
			'component.html')

	except ObjectDoesNotExist, e:
		return HttpResponseNotFound("Error 404: component: " + ref)
#
#
def GetManufacturers(request):
	format = request.GET.get('format', 'html')

	if format == 'json':
		return HttpResponse (
			simplejson.dumps(datautils.GetManufacturersInfoAsList() ),
			mimetype='application/json'
							)
	elif format == 'xml':
		params = { 'manufacturers' : datautils.GetManufacturersInfoAsList() }
		return HttpResponse (
			render_to_string('manufacturers.xml', params),
			mimetype='application/xml'
							)

	elif format == 'html':
		return HttpResponse("HTML for manufacturers :D")

	else:
		return HttpResponseBadRequest(
			'Wrong parameter "format" [html, xml, json]')


#
#
def GetManufacturer(request, name):
	format = request.GET.get('format', 'html')

	try:

		if format == 'json':
			return HttpResponse (
				simplejson.dumps(datautils.GetManufacturerInfo(name) ),
				mimetype='application/json'
								)
		elif format == 'xml':
			params = { 'manufacturer' : datautils.GetManufacturerInfo(name)}
			return HttpResponse (
				render_to_string('manufacturer.xml', params),
				mimetype='application/xml'
								)

		elif format == 'html':
			return HttpResponse("HTML for manufacturers :D")

		else:
			return HttpResponseBadRequest(
				'Wrong parameter "format" [html, xml, json]')

	except ObjectDoesNotExist:
		return HttpResponseNotFound(
			"Manufacturer with name: " + name + ", does not exists")

#
#
def GetCategories(request):
	format = request.GET.get('format', 'html')

	if format == 'json':
		return HttpResponse(
			simplejson.dumps(datautils.GetCategoriesInfoAsList()),
			mimetype='application/json')

	elif format == 'xml':
		params = { 'categories' : datautils.GetCategoriesInfoAsList() }
		return HttpResponse(
			render_to_string('categories.xml', params),
			mimetype='application/xml')

	elif format == 'html':
		return HttpResponse("HTML for manufacturers :D")

	else:
		return HttpResponseBadRequest(
				'Wrong parameter "format" [html, xml, json]')

#
#
def GetCategory(request, name):
	
	try:

		format = request.GET.get('format', 'html')

		if format == 'json':
			return HttpResponse(
				simplejson.dumps(datautils.GetCategoryComponentsList(name)),
				mimetype='application/json')

		elif format == 'xml':
			params = { 'components' : datautils.GetCategoryComponentsList(name)}
			return HttpResponse(
				render_to_string('components.xml', params),
				mimetype='application/xml')

		elif format == 'html':
			return HttpResponse("HTML for manufacturers :D")
			
		else:
			return HttpResponseBadRequest(
					'Wrong parameter "format" [html, xml, json]')

	except ObjectDoesNotExist:
		return HttpResponseNotFound(
			"Category with name: " + name + ", does not exists")