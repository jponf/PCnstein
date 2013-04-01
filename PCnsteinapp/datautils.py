# -*- coding: utf-8 -*-

import models
import globdata

#
#
def GetComponentsInfoAsList():
	"""
	GetComponentsInfoAsList() -> Return a list fillet with dictionaries
								containing component information
	"""
	cinf = []

	for c in models.Component.objects.all():
		cinfo = { 'ref' : c.ref, 'name' : c.name, 'desc' : c.desc, 
				  'avg_price' : str(c.avg_price), 'category' : c.category,
				  'img' : str(c.img),
				  'links' : { 'rel' : 'self', 
				  			  'href' : '%s/%s/%s' % (globdata.API_URL,
				  			  						 globdata.API_COMPONENTS,
				  			  						 c.ref) } }
		cinf.append(cinfo)
	return cinf

#
#
def GetComponentInfo(ref):

	comp = models.Component.objects.get(pk=ref)

	cinf = [
		{ 	
			'ref': comp.ref, 'name' : comp.name, 'desc' : comp.desc,
			'avg_price' : str(comp.avg_price), 'category' : c.category,
			'img' : str(comp.img), 'links' : { 'rel' : 'self' }
		}
	]

	return cinf

#
#
def GetManufacturersInfoAsList():

	manu_info = []

	for m in models.Manufacturer.objects.all():
		single_manu_info = { 
						'name': m.name, 
						'desc': m.desc, 
						'links': { 
									'rel': self, 
									'href': '%s/%s/%s' % (globdata.API_URL, globdata.API_MANUFACTURERS, m.ref)
								 }
					}

		manu_info.append(single_manu_info)

	return manu_info

#
#
def GetManufacturersInfo(name):

	manufacturer = models.Manufacturer.objects.get(pk=name)

	manu_info = [{'name': manufacturer.name, 'desc': manufacturer.desc}, 'links': {'rel': 'self'}]

	return manu_info


