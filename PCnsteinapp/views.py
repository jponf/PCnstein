# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.core import serializers
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

import models
import datautils


#
#
def GetMainPage(request):
	return render_to_response('mainpage.html')

#
#
def GetComponents(request):
	format = request.GET.get('format', 'html')

	if format == 'json':
		return HttpResponse (
			simplejson.dumps( datautils.GetComponentsInfoAsList() ),
			mimetype='application/json' 
							)
		
	elif format == 'xml':
		params = { 'components': datautils.GetComponentsInfoAsList() }
		return HttpResponse ( 
			render_to_string('components.xml', params), 
			mimetype='application/xml'
							)

	elif format == 'html':
		params = { 'pagetitle' : "Components"}
		params['cinfo'] = datautils.GetComponentsInfoAsList()
		return render_to_response('components.html', params)

	else:
		return HttpResponseBadRequest(
			'Wrong parameter "format" [html, xml, json]')

#
#
def GetComponent(request, ref):
	format = request.GET.get('format', 'html')

	if format == 'json':
		return HttpResponse(
			simplejson.dumps(datautils.GetComponentInfo(ref)) )

	elif format == 'xml':
		params = { 'component' : datautils.GetComponentInfo(ref) }
		return HttpResponse(
				render_to_string('component.xml', params),
				mimetype='application/xml'
							)

	elif format == 'html':
		return HttpResponse('HTML for component ' + ref)

	else:
		return HttpResponseBadRequest(
			'Wrong parameter "format" [html, xml, json]')

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