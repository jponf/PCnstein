# Create your views here.
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers

import models
import datautils


#
#
def GetMainPage(request):
	format = request.GET.get('format', 'http')

	return render_to_response('mainpage.html')

#
#
def GetComponents(request):
	format = request.GET.get('format', 'http')

	if format == 'json':
		#json = serializers.serialize('json', models.Component.objects.all())
		#return HttpResponse(json, mimetype='application/json')
		return HttpResponse(
			simplejson.dumps( datautils.GetComponentsInfoAsList() ),
			mimetype='application/json' )
		
	elif format == 'xml':
		# xml = serializers.serialize('xml', models.Component.objects.all())
		# return HttpResponse(xml, mimetype='application/xml')
		return HttpResponse(render_to_string('components.xml', 
				{'components': models.Component.objects.all()}))
	elif format == 'http':
		params = { 'pagetitle' : "Components"}
		params['cinfo'] = datautils.GetComponentsInfoAsList()

		return render_to_response('components.html', params)
	else:
		return HttpResponseBadRequest('Bad Format')

#
#
def GetComponent(request, ref):
	format = request.GET.get('format', 'http')

	if format == 'json':
		return HttpResponse(
			simplejson.dumps( datautils.GetComponentInfo(ref)) )
	elif format == 'xml':
		pass # TODO
	elif format == 'http':
		pass # TODO
	else:
		return HttpResponseBadRequest('Bad Format')