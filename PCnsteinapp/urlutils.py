# -*- coding: utf-8 -*-

import globdata
from urllib import pathname2url

#
#
def getComponentURL(ref):
	if ref:
		return getApiURL(globdata.API_COMPONENTS, pathname2url(ref))
	else:
		return ''

#
#
def getManufacturerURL(name):
	if name:
		return getApiURL(globdata.API_MANUFACTURERS, pathname2url(name))
	else:
		return ''

#
#
def getCategoryURL(name):
	if name:
		return getApiURL(globdata.API_CATEGORIES, pathname2url(name))
	else:
		return ''

#
#
def getOperatingSystemURL(name):
	if name:
		return getApiURL(globdata.API_OS, pathname2url(name))
	else:
		return ''

#
#
def getApiURL(*args):
	return globdata.API_URL + '/' + "/".join(args)