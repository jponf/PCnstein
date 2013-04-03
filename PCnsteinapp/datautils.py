# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from urlutils import GetComponentURL, GetManufacturerURL, GetCategoryURL, \
					GetOperatingSystemURL

import sys
import models
import globdata


#
#
def GetComponentsSummaryAsList():
	"""
	GetComponentsSummaryAsList() -> Return a list filled with dictionaries
								containing component information
	"""
	cinf = []

	for c in models.Component.objects.all():
		cinfo = { 'ref' : c.ref, 'name' : c.name, 'img' : str(c.img),
				  'avgprice' : str(c.avgprice), 'category' : str(c.category),
				  'manufacturer' : '',
				  'links' : [ { 'rel' : 'self', 
				  			 	'href': GetComponentURL(c.ref) },
				  			  { 'rel' : 'category',
				  			  	'href' : GetCategoryURL(c.category.name) },				  			  
				  			]
				}

		# Add manufacturer if it exists
		manufacturer = GetComponentManufacturer(c)
		if manufacturer:
			cinfo['manufacturer'] = manufacturer.name
			cinfo['links'].append({ 'rel' : 'manufacturer',
								'href' : GetManufacturerURL(manufacturer.name)})

		# Append info to the list
		cinf.append(cinfo)

	return cinf

#
#
def GetComponentInfo(ref):
	"""
	GetComponentInfo(ref) -> Return a dictionary with all the information
							of the specified component
	"""
	comp = models.Component.objects.get(pk=ref)

	cinf = \
		{ 	
			'ref': comp.ref, 'name' : comp.name, 'img' : str(comp.img),
			'avgprice' : str(comp.avgprice), 'category': str(comp.category),
			'desc' : comp.desc,
			'manufacturer' : '',
			'supportedby' : '',
			'links' : [ { 'rel' : 'self',
						  'href' : GetComponentURL(comp.ref) }
					  ]
		}

	# Add manufacturer if it exists
	manufacturer = GetComponentManufacturer(comp)
	if manufacturer:
		cinf['manufacturer'] = manufacturer.name
		cinf['links'].append({ 'rel' : 'manufacturer',
							'href' : GetManufacturerURL(manufacturer.name)})

	# Add supported by list if exists (elements separed by ;)
	supportedby = GetComponentSupportedBy(comp)
	supportedbystr = ';'.join(s.os.name for s in supportedby)
		
	if supportedbystr:
		cinf['supportedby'] = supportedbystr
		for s in supportedby:
			cinf['links'].append( { 'rel' : 'supportedby',
									'href' : GetOperatingSystemURL(s.os.name) })
			
	return cinf

#
#
def GetComponentManufacturer(comp):
	"""
	GetComponentManufacturer(comp)-> Return the manufacturer instance associated
								with the specified component
	"""

	# Try get the relation with the manufacturer
	try:
		madeby = models.CMadeBy.objects.get(component_id=comp)
		return madeby.manufacturer
	except ObjectDoesNotExist:
		sys.stderr.write('No Made By relationship for component: ' + str(comp))
		return None

#
#
def GetComponentSupportedBy(comp):
	"""
	GetComponentSupportedBy(comp) -> Return the OS that support the specified
								component
	"""

	# Try to get the supportedby relations
	return models.SupportedBy.objects.filter(component_id=comp)
	


#
#
def GetManufacturersInfoAsList():
	"""
	GetManufacturersInfoAsList() -> Return a list filled with dictionaries
								containing manufacturers information
	"""
	manu_info = []

	for m in models.Manufacturer.objects.all():
		single_manu_info = { 
						'name': m.name, 
						'desc': m.desc, 
						'links': { 
									'rel': 'self', 
									'href': '%s/%s/%s' % (globdata.API_URL, 
												globdata.API_MANUFACTURERS,
												m.name)
								 }
					}

		manu_info.append(single_manu_info)

	return manu_info

#
#
def GetManufacturerInfo(name):
	"""
	GetManufacturerInfo(name) -> Return a dictionary with all the information
								related to the specified manufacturer
	"""
	# TODO add list of made components/operating systems
	manufacturer = models.Manufacturer.objects.get(pk=name)

	manu_info = \
		{
			'name': manufacturer.name, 'desc': manufacturer.desc,
			'links': {'rel': 'self'}
		}

	return manu_info

#
#
def GetCategoriesInfoAsList():
	"""
	GetCategoriesInfoAsList() -> Return a list filled dictionaries containing
								categories information
	"""
	Get
	categories = []

	for cat in models.Category.objects.all():
		categories.append( { 'name' : cat.name	} )

	return categories

#
#
def GetCategoryComponentsList(name):
	"""
	GetCategoryComponentsList(name) -> Return a list filled with dictionaries 
								with information of all components under 
								the given category
	"""
	category = models.Category.objects.get(pk=name)	
	components = models.Component.objects.filter(category=category)
	cinf = []

	for c in components:
		cinfo = { 'ref' : c.ref, 'name' : c.name, 'desc' : c.desc, 
				  'avg_price' : str(c.avg_price), 'category' : str(c.category),
				  'img' : str(c.img),
				  'links' : { 'rel' : 'self', 
				  			  'href' : '%s/%s/%s' % (globdata.API_URL,
				  			  						 globdata.API_COMPONENTS,
				  			  						 c.ref) } }
		cinf.append(cinfo)
	return cinf