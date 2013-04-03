# -*- coding: utf-8 -*-

import globdata
from urllib import pathname2url

#
#
def GetComponentURL(ref):
	if ref:
		return GetApiURL(globdata.API_COMPONENTS, pathname2url(ref))
	else:
		return ''

#
#
def GetManufacturerURL(name):
	if name:
		return GetApiURL(globdata.API_MANUFACTURERS, pathname2url(name))
	else:
		return ''

#
#
def GetCategoryURL(name):
	if name:
		return GetApiURL(globdata.API_CATEGORIES, pathname2url(name))
	else:
		return ''

#
#
def GetOperatingSystemURL(name):
	if name:
		return GetApiURL(globdata.API_OS, pathname2url(name))
	else:
		return ''

#
#
def GetApiURL(*args):
	return globdata.API_URL + '/' + "/".join(args)