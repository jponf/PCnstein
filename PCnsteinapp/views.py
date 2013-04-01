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
		params = { 'components': models.Component.objects.all() }
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
			simplejson.dumps( datautils.GetComponentInfo(ref)) )

	elif format == 'xml':
		return HttpResponse('XML for component ' + ref)

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
		params = { 'manufacturers' : models.Manufacturer.objects.all() }
		return HttpResponse (
			render_to_string('manufacturers.xml', params),
			mimetype='application/xml'
							)

	elif format == 'http'
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
				simplejson.dumps(datautils.GetManufacturersInfoAsList() ),
				mimetype='application/json'
								)
		elif format == 'xml':
			params = { 'manufacturers' : models.Manufacturer.objects.all() }
			return HttpResponse (
				render_to_string('manufacturers.xml', params),
				mimetype='application/xml'
								)

		elif format == 'http'
			return HttpResponse("HTML for manufacturers :D")

		else:
			return HttpResponseBadRequest(
				'Wrong parameter "format" [html, xml, json]')

	except ObjectDoesNotExist, e:
		return HttpResponseNotFound(
			"Manufacturer with name: " + name + ", does not exists")