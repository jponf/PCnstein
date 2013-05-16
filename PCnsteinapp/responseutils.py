# -*- coding: utf-8 -*-

from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, HttpResponseNotFound, \
						HttpResponseForbidden

#
#
def getHttpResponseForbiddenHTML(pagetitle, user, reason):
	"""
	Returns the default forbidden action web page
	"""
	response_str = render_to_string('forbidden.html', 
									{ 'pagetitle' : pagetitle,
									  'user' : user,
								  	  'reason' : reason })

	return HttpResponseForbidden(response_str)

#
#
def getHttpResponseNotFoundHTML(pagetitle, user, resource, resource_url):
	"""
	Returns the default resource not found web page
	"""
	response_str = render_to_string('notfound.html',
									{ 'pagetitle' : pagetitle,
									  'user' : user,
									  'resource' : resource,
									  'url' : resource_url })

	return HttpResponseNotFound(response_str)
