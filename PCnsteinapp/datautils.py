# -*- coding: utf-8 -*-

import models
import globdata

#
#
def GetComponentsInfoAsList():
	"""
	GetComponentsInfoAsList() -> Return a list filled with dictionaries
								containing component information
	"""
	cinf = []

	for c in models.Component.objects.all():
		cinfo = { 'ref' : c.ref, 'name' : c.name, 'desc' : c.desc, 
				  'avg_price' : str(c.avg_price), 'category' : str(c.category),
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
	"""
	GetComponentInfo(ref) -> Return a dictionary with all the information
							of the specified component
	"""
	comp = models.Component.objects.get(pk=ref)

	cinf = \
		{ 	
			'ref': comp.ref, 'name' : comp.name, 'desc' : comp.desc,
			'avg_price' : str(comp.avg_price), 'category' : str(comp.category),
			'img' : str(comp.img), 'manufacturer' : '', 
			'links' : { 'rel' : 'self',
						'manufacturer' : '' }
		}

	# Try to add information about the manufacturer
	try:
		madeby = models.CMadeBy.objects.get(component_id=comp)
		manu = madeby.manufacturer
		cinf['manufacturer'] = madeby.manufacturer.name
		cinf['links']['manufacturer'] = '%s/%s/%s/' % (globdata.API_URL,
													 globdata.API_MANUFACTURERS,
													 manu.name)
	except:
		pass
	
	return cinf

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