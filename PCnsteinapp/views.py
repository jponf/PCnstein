# Create your views here.
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers

import models

#
#
def GetComponentsInfoAsList():
	cinf = []

	for c in models.Component.objects.all():
		cinfo = { 'ref' : c.ref, 'name' : c.name, 'desc' : c.desc, 
				  'avg_price' : str(c.avg_price), 'category' : c.category }
		cinf.append(cinfo)
	return cinf

#
#
def GetComponents(request):
	format = request.GET.get('format', 'http')

	if format == 'json':
		#json = serializers.serialize('json', models.Component.objects.all())
		#return HttpResponse(json, mimetype='application/json')
		return HttpResponse(simplejson.dumps(GetComponentsInfoAsList()),
							mimetype='application/json')
		
	elif format == 'xml':
		# xml = serializers.serialize('xml', models.Component.objects.all())
		# return HttpResponse(xml, mimetype='application/xml')
		return HttpResponse(render_to_string('components.xml', 
				{'components': models.Component.objects.all()}))
	elif format == 'http':
		return HttpResponse('HTTP')
	else:
		return HttpResponse('Error madafaka')

#
#
def GetComponent(request, ref):
	return HttpResponse(ref)
