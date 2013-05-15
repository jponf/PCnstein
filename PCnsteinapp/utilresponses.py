# -*- coding: utf-8 -*-

from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, HttpResponseNotFound, \
						HttpResponseForbidden

def HttpResponseForbiddenHTML(pagetitle, reason):
	response_str = render_to_string('forbidden.html', 
									{ 'pagetitle' : pagetitle,
								  	  'reason' : reason })

	return HttpResponseForbidden(response_str)

