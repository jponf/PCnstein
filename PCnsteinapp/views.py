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
def GenerateResponse(request, data, datatag=None, xmltemplate=None,
					htmltemplate=None, htmlargs={}):
	"""
	TODO
	"""
	response = None
	format = request.GET.get('format', 'html')

	if format == 'json':
		response = HttpResponse(simplejson.dumps(data),
								mimetype='application/json')		

	elif format == 'xml':
		if not datatag:
			raise Exception("datatag must be specified to generate an xml response")

		xmlstr = ''
		if xmltemplate:
			xmlstr = render_to_string(xmltemplate, { datatag : data } )
		else:
			if isinstance(data, list) or isinstance(data, tuple):
				xmlstr = dict2xml( { datatag : data }, datatag )
			else:
				xmlstr = dict2xml(data, datatag)

		response = HttpResponse(xmlstr, mimetype='application/xml')

	elif format == 'html':
		if not htmltemplate:
			raise Exception("htmltemplate must be specified to generate an "
				"html response")
		if not isinstance(htmlargs, dict):
			raise Exception("htmlargs must be a dictionary")

		htmlargs[datatag] = data

		response = render_to_response(htmltemplate, htmlargs)
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
					'components.html', 
					{'pagetitle' : 'Components'})		

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

	return GenerateResponse(request,
					datautils.GetManufacturersInfoAsList(),
					'manufacturers',
					None,
					'manufacturers.html')

#
#
def GetManufacturer(request, name):
	try:
		return GenerateResponse(request,
			datautils.GetManufacturerInfo(name),
			'manufacturer',
			None,
			'manufacturer.html')

	except ObjectDoesNotExist:
		return HttpResponseNotFound(
			"Manufacturer with name '" + name + "' does not exist")

#
#
def GetCategories(request):
	return GenerateResponse(request,
		datautils.GetCategoriesInfoAsList(),
		'categories',
		None,
		'categories.html')

#
#
def GetCategory(request, name):
	
	try:
		return GenerateResponse(request,
			datautils.GetCategoryComponentsList(name),
			'components',
			None,
			'components.html',
			{ 'pagetitle' : '[%s] Components' % name } )
		
	except ObjectDoesNotExist:
		return HttpResponseNotFound(
			"Category with name '" + name + "' does not exist")

#
#
def GetOSes(request):
	return GenerateResponse(request,
		datautils.GetOSInfoAsList(),
		'os',
		None,
		'os.html')

#
#
def GetOS(request, name):

	try:
		return GenerateResponse(request,
			datautils.GetOSInfo(name),
			'os',
			None,
			'os.html')
		
	except ObjectDoesNotExist:
		return HttpResponseNotFound(
			"Operating system with name '" + name + "' does not exist")