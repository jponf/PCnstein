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
def getCreateComponentURL():
	return getApiURL(globdata.API_CREATE_COMPONENT)

#
#
def getModifyComponentURL(ref):
	if ref:
		return getApiURL(globdata.API_MODIFY_COMPONENT, pathname2url(ref))
	else:
		return ''

#
#
def getDeleteComponentURL(ref):
	if ref:
		return getApiURL(globdata.API_DELETE_COMPONENT, pathname2url(ref))
	else:
		return ''

#
#
def getAddSupportedByURL(ref):
	if ref:
		return getApiURL(globdata.API_ADD_SUPPORTEDBY, pathname2url(ref))
	else:
		return ''

#
#
def getDeleteSupportedByURL(id):
	if id:
		return getApiURL(globdata.API_DELETE_SUPPORTEDBY, pathname2url(str(id)))
	else:
		return ''

#
#
def getCreateComponentReviewURL(ref):
	if ref:
		return getApiURL(globdata.API_CREATE_COMPONENT_REVIEW, ref)
	else:
		return ''

#
#
def getUserURL():
	return getApiURL(globdata.API_USER)

#
#
def getDeleteUserURL(id):
	if id:
		return getApiURL(globdata.API_DELETE_USER, str(id))
	else:
		return ''

#
#
def getApiURL(*args):
	return globdata.API_URL + '/' + "/".join(args)
