# -*- coding: utf-8 -*-

from django.utils import simplejson
from django.http import HttpResponse

import re
import urllib2

GEO_LOCALIZATION_URL = 'http://smart-ip.net/geoip-json/'
#
# 
def getGeoInformationByIP(request):
	clientip = getClientIP(request)
	con = None
	if isPrivateIP(clientip):
		con = urllib2.urlopen(GEO_LOCALIZATION_URL)
	else:
		print 'hello'
		con = urllib2.urlopen(GEO_LOCALIZATION_URL + clientip)
	
	strdata = con.read()
	data = simplejson.loads(strdata)
	responsedata = {}

	print strdata

	if data.has_key('error'):
		responsedata['error'] = 'Cannot request host information'
	else:
		responsedata['country_name'] = data['countryName']
		responsedata['region'] = data['region']
		responsedata['city'] = data['city']

	return HttpResponse(simplejson.dumps(responsedata), 
						content_type='application/json')


#
#
def isPrivateIP(ip):
	private10 = re.compile('\b*10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b*')
	private172 = re.compile('\b*172\.16\.\d{1,3}\.\d{1,3}\b*')
	private192 = re.compile('\b*192\.168\.\d{1,3}\.\d{1,3}\b*')
	localhost = re.compile('\b*127.0.0.1\b*')

	print ip

	if private10.match(ip) or private172.match(ip) or private192.match(ip) or \
		localhost.match(ip):
		return True

	return False

#
#
def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
