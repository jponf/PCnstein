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
	print supportedby
	if supportedby:
		supportedbystr = ';'.join(os.name for os in supportedby)
		cinf['supportedby'] = supportedbystr
		for os in supportedby:
			cinf['links'].append( { 'rel' : 'supportedby',
									'href' : GetOperatingSystemURL(os.name) })
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
		return [s.os for s in models.SupportedBy.objects.filter(
															component_id=comp)]
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
							 'links': [ { 'rel': 'self', 
										 'href': GetManufacturerURL(m.name)}
								 	  ]
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
			'links': [ { 'rel' : 'self',
						 'href' : GetManufacturerURL(manufacturer.name) }
					 ] 
		}

	# Try to add links of made components
	components = GetManufacturerComponents(manufacturer)

	for c in components:
		manu_info['links'].append({ 'rel' : 'makes',
									'href' : GetComponentURL(c.name) })

	# Try to add links of made operating systems
	operating_systems = GetManufacturerOperatingSystems(manufacturer)

	for os in operating_systems:
		manu_info['links'].append({ 'rel' : 'makes',
									'href' : GetOperatingSystemURL(os.name) })

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
							 'links' : [ 
							 				{ 
							 					'rel' : 'self',
							 					'href': GetCategoryURL(cat.name) 
							 				}
							 		   ]
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
def GetOSInfoAsList():
	"""
	GetOSInfoAsList() -> Return a list filled with dictionaries
								containing OS information
	"""

	os_info = []

	for os in models.OperatingSystem.objects.all():
		os = { 'name': os.name,
			   'links': [ 
			   				{ 
			   					'rel': 'self',
			   					'href': GetOperatingSystemURL(os.name)
			   				}
			   			]
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
				'links' : [ 
							{ 
							  'rel' : 'self', 
		  		   		 	  'href': GetOperatingSystemURL(os.name) 
		  		   		 	}			  			  
		  				  ]
			  }

	manufacturer = GetOSManufacturer(os)
	if manufacturer:
		os_info['manufacturer'] = manufacturer.name
		os_info['links'].append({ 
								'rel' : 'manufacturer',
								'href' : GetManufacturerURL(manufacturer.name)
								})


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