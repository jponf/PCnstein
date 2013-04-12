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
				  'avgprice' : str(c.avgprice), 
				  'category' : { 'name' : str(c.category),
				  				 'link' : GetCategoryURL(c.category.name)}  if c.category else '',
				  'manufacturer' : {},
				  'link' : { 'rel' : 'self', 
				  			 'href': GetComponentURL(c.ref) },			  			  
				  			
				}

		# Add manufacturer if it exists
		manufacturer = GetComponentManufacturer(c)
		if manufacturer:
			cinfo['manufacturer'] =  { 'name' :  manufacturer.name, 
									   'link' :  GetManufacturerURL(manufacturer.name) }

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
			'avgprice' : str(comp.avgprice), 
			'category' : { 'name' : str(comp.category), 
				    	   'link' : GetCategoryURL(comp.category.name)}  if comp.category else '',
			'desc' : comp.desc,
			'manufacturer' : '',
			'supportedby' : [],
			'link' : { 'rel' : 'self',
					   'href' : GetComponentURL(comp.ref) }
					  
		}

	# Add manufacturer if it exists
	manufacturer = GetComponentManufacturer(comp)
	if manufacturer:
		cinf['manufacturer'] =  { 'name' :  manufacturer.name, 
								  'link' :  GetManufacturerURL(manufacturer.name) }
	

	# Add supported by list if exists (elements separed by ;)
	supportedby = GetComponentSupportedBy(comp)

	if supportedby:
		# supportedbystr = [(	s['os'],
		# 				 	s['minversion'],
		# 				 	s['maxversion']) 
		# 				  for s in supportedby]
		#cinf['supportedby'] = supportedby
		
		for sb in supportedby:
			cinf['supportedby'].append({ 'name' : sb['name'],
										 'link' : GetOperatingSystemURL(sb['name']),
										 'minversion' : sb['minversion'],
										 'maxversion' : sb['maxversion']})
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
	try:
		return [ {'name': s.os.name, 
				  'minversion' : s.minversion if s.minversion else '',
				  'maxversion' : s.maxversion if s.maxversion else ''} 
				for s in models.SupportedBy.objects.filter(component_id=comp) ]
	except ObjectDoesNotExist:
		return None

#
#
def GetManufacturersInfoAsList():
	"""
	GetManufacturersInfoAsList() -> Return a list filled with dictionaries
								containing manufacturers information
	"""
	manu_info = []

	for m in models.Manufacturer.objects.all():
		single_manu_info = { 'name': m.name,  
							 'link': { 'rel': 'self', 
									   'href': GetManufacturerURL(m.name)}
								 	
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
	manufacturer = models.Manufacturer.objects.get(pk=name)

	manu_info = \
		{
			'name': manufacturer.name, 'desc': manufacturer.desc,
			'link': { 'rel' : 'self',
					  'href' : GetManufacturerURL(manufacturer.name) },
			'makes' : []
		}

	# Try to add links of made components
	components = GetManufacturerComponents(manufacturer)

	for c in components:
		manu_info['makes'].append({ 'name' : c.name,
									'link' : GetComponentURL(c.name) })

	# Try to add links of made operating systems
	operating_systems = GetManufacturerOperatingSystems(manufacturer)

	for os in operating_systems:
		manu_info['makes'].append({ 'name' : os.name,
									'link' : GetOperatingSystemURL(os.name) })

	return manu_info

#
#
def GetManufacturerComponents(manufacturer):
	return [sb.component for sb in 
				models.CMadeBy.objects.filter(manufacturer_id=manufacturer)]

#
#
def GetManufacturerOperatingSystems(manufacturer):
	return [osmb.os for osmb in
				models.OSMadeBy.objects.filter(manufacturer_id=manufacturer)]
#
#
def GetCategoriesInfoAsList():
	"""
	GetCategoriesInfoAsList() -> Return a list filled dictionaries containing
								categories information
	"""
	categories = []

	for cat in models.Category.objects.all():
		components = models.Component.objects.filter(category_id=cat)
		categories.append( { 'name' : cat.name,
							 'itemcount' : len(components), 
							 'link' : { 
							 					'rel' : 'self',
							 					'href': GetCategoryURL(cat.name) 
							 		  }
						   } )

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
	components = models.Component.objects.filter(category_id=category)
	cinf = []

	for c in components:
		cinfo = { 'ref' : c.ref, 'name' : c.name, 'img' : str(c.img),
				  'avgprice' : str(c.avgprice), 
				  'category' : { 'name' : str(c.category), 
				  				 'link' : GetCategoryURL(c.category.name)},
				  'manufacturer' : '',
				  'link' : { 'rel' : 'self', 
				  			 'href': GetComponentURL(c.ref) }			  			  
				}

		# Add manufacturer if it exists
		manufacturer = GetComponentManufacturer(c)
		if manufacturer:
			cinfo['manufacturer'] =  { 'name' :  manufacturer.name, 
									   'link' :  GetManufacturerURL(manufacturer.name) }

		# Append info to the list
		cinf.append(cinfo)

	return cinf

#
#
def GetOSInfoAsList():
	"""
	GetOSInfoAsList() -> Return a list filled with dictionaries
								containing OS information
	"""

	os_info = []

	for os in models.OperatingSystem.objects.all():
		os = { 'name': os.name,
			   'link': { 'rel': 'self',
			   					'href': GetOperatingSystemURL(os.name) }
			 }

		os_info.append(os)

	return os_info

#
#
def GetOSInfo(name):
	"""
	GetOSInfo(name) -> Return a dictionary with all the information
							of the specified OS
	"""

	print name
	os = models.OperatingSystem.objects.get(pk=name)
	os_info = { 'name' : os.name, 
				'manufacturer' : '',
				'link' :   { 
							  'rel' : 'self', 
		  		   		 	  'href': GetOperatingSystemURL(os.name) 
		  		   		 	}			  			  
			  }

	manufacturer = GetOSManufacturer(os)
	if manufacturer:
		os_info['manufacturer'] =  { 'name' :  manufacturer.name, 
								     'link' :  GetManufacturerURL(manufacturer.name) }


	return os_info

def GetOSManufacturer(os):
	"""
	GetOSManufacturer(os)-> Return the manufacturer instance associated
								with the specified OS
	"""

	try:
		madeby = models.OSMadeBy.objects.get(os_id=os)
		return madeby.manufacturer
	except ObjectDoesNotExist:
		sys.stderr.write('No Made By relationship for operating system: ' + str(os))
		return None