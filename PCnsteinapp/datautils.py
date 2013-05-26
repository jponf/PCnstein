# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from urlutils import getComponentURL, getManufacturerURL, getCategoryURL, \
                    getOperatingSystemURL

import sys
import models
import globdata


#
#
def getComponentsSummaryAsList():
    """
    getComponentsSummaryAsList() -> Return a list filled with dictionaries
                                containing component information
    """
    cinf = []

    for c in models.Component.objects.all():
        cinfo = \
            { 
            'ref' : c.ref, 'name' : c.name, 'img' : str(c.img),
            'avgprice' : str(c.avgprice), 
            'category' : { 
                'name' : str(c.category) if c.category else '',
                'link' : getCategoryURL(c.category.name) if c.category else ''},
            'manufacturer' : { 
                'name' : str(c.manufacturer) if c.manufacturer else '',
                'link' : getManufacturerURL(c.manufacturer.name) if c.manufacturer else ''},
            'link' : {  'rel' : 'self', 
                        'href': getComponentURL(c.ref) },                        
            }

        # Append info to the list
        cinf.append(cinfo)

    return cinf

#   
#
def getComponentInfo(ref):
    """
    getComponentInfo(ref) -> Return a dictionary with all the information
                            of the specified component
    """
    comp = models.Component.objects.get(pk=ref)

    cinf = \
        {   
            'ref': comp.ref, 'name' : comp.name, 'img' : str(comp.img),
            'avgprice' : str(comp.avgprice), 
            'category' : { 
                    'name' : str(comp.category) if comp.category else '',
                    'link' : getCategoryURL(comp.category.name) if comp.category else ''},
            'desc' : comp.desc,
            'manufacturer' : { 
                    'name' : str(comp.manufacturer) if comp.manufacturer else '',
                    'link' : getManufacturerURL(comp.manufacturer.name) if comp.manufacturer else ''},
            'supportedby' : [],
            'createdby' : str(comp.createdby),
            'link' : { 'rel' : 'self',
                       'href' : getComponentURL(comp.ref) } 
        }
    

    # Add supported by list if exists (elements separed by ;)
    supportedby = getComponentSupportedBy(comp)

    if supportedby:
        for sb in supportedby:
            cinf['supportedby'].append({ 'id' : sb['id'],
                                         'name' : sb['name'],
                                         'link' : getOperatingSystemURL(sb['name']),
                                         'minversion' : sb['minversion'],
                                         'maxversion' : sb['maxversion']})

    # Add reviews
    cinf['reviews'] = getComponentReviews(comp)

    return cinf

#
#
def getComponentSupportedBy(comp):
    """
    getComponentSupportedBy(comp) -> Return the OS that support the specified
                                component
    """
    try:
        return [ {'name': s.os.name, 
                  'minversion' : s.minversion if s.minversion else '',
                  'maxversion' : s.maxversion if s.maxversion else '',
                  'id' : s.id} 
                for s in models.SupportedBy.objects.filter(component_id=comp) ]
    except ObjectDoesNotExist:
        return None

#
#
def getManufacturersInfoAsList():
    """
    getManufacturersInfoAsList() -> Return a list filled with dictionaries
                                containing manufacturers information
    """
    manu_info = []

    for m in models.Manufacturer.objects.all():
        single_manu_info = { 'name': m.name,  
                             'link': { 'rel': 'self', 
                                       'href': getManufacturerURL(m.name)}
                                    
                            }                       

        manu_info.append(single_manu_info)

    return manu_info

#
#
def getManufacturerInfo(name):
    """
    getManufacturerInfo(name) -> Return a dictionary with all the information
                                related to the specified manufacturer
    """
    manufacturer = models.Manufacturer.objects.get(pk=name)

    manu_info = \
        {
            'name': manufacturer.name, 'desc': manufacturer.desc,
            'link': { 'rel' : 'self',
                      'href' : getManufacturerURL(manufacturer.name) },
            'makes' : []
        }

    # Try to add links of made components
    components = getManufacturerComponents(manufacturer)

    for c in components:
        manu_info['makes'].append({ 'name' : c.name,
                                    'link' : getComponentURL(c.name) })

    # Try to add links of made operating systems
    operating_systems = getManufacturerOperatingSystems(manufacturer)

    for os in operating_systems:
        manu_info['makes'].append({ 'name' : os.name,
                                    'link' : getOperatingSystemURL(os.name) })

    return manu_info

#
#
def getManufacturerComponents(manufacturer):
    return [sb for sb in 
                models.Component.objects.filter(manufacturer_id=manufacturer)]

#
#
def getManufacturerOperatingSystems(manufacturer):
    return [osmb.os for osmb in
                models.OSMadeBy.objects.filter(manufacturer_id=manufacturer)]
#
#
def getCategoriesInfoAsList():
    """
    getCategoriesInfoAsList() -> Return a list filled dictionaries containing
                                categories information
    """
    categories = []

    for cat in models.Category.objects.all():
        components = models.Component.objects.filter(category_id=cat)
        categories.append( { 'name' : cat.name,
                             'itemcount' : len(components), 
                             'link' : { 
                                                'rel' : 'self',
                                                'href': getCategoryURL(cat.name) 
                                      }
                           } )

    return categories

#
#
def getCategoryComponentsList(name):
    """
    getCategoryComponentsList(name) -> Return a list filled with dictionaries 
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
                                 'link' : getCategoryURL(c.category.name)},
                  'manufacturer' : { 
                    'name' : str(c.manufacturer) if c.manufacturer else '',
                    'link' : getManufacturerURL(c.manufacturer.name) if c.manufacturer else ''},
                  'link' : { 'rel' : 'self', 
                             'href': getComponentURL(c.ref) }                         
                }

        # Append info to the list
        cinf.append(cinfo)

    return cinf

#
#
def getOSsInfoAsList():
    """
    getOSInfoAsList() -> Return a list filled with dictionaries
                                containing OS information
    """

    os_info = []

    for os in models.OperatingSystem.objects.all():
        os = { 'name': os.name,
               'link': { 'rel': 'self',
                                'href': getOperatingSystemURL(os.name) }
             }

        os_info.append(os)

    return os_info

#
#
def getOSInfo(name):
    """
    getOSInfo(name) -> Return a dictionary with all the information
                            of the specified OS
    """

    print name
    os = models.OperatingSystem.objects.get(pk=name)
    os_info = { 'name' : os.name, 
                'manufacturer' : '',
                'link' :   { 
                              'rel' : 'self', 
                              'href': getOperatingSystemURL(os.name) 
                            }                         
              }

    manufacturer = getOSManufacturer(os)
    if manufacturer:
        os_info['manufacturer'] =  { 'name' :  manufacturer.name, 
                                     'link' :  getManufacturerURL(manufacturer.name) }


    return os_info

#
#
def getOSManufacturer(os):
    """
    getOSManufacturer(os)-> Return the manufacturer instance associated
                                with the specified OS
    """

    try:
        madeby = models.OSMadeBy.objects.get(os_id=os)
        return madeby.manufacturer
    except ObjectDoesNotExist:
        sys.stderr.write('No Made By relationship for operating system: ' + str(os))
        return None

#
#
def getComponentReviews(comp):
    """
    getComponentReviews(comp) -> Return a list filled with all the reviews of
                                    of the specified component
    """

    reviews = []
    try:
        
        for r in models.ComponentReview.objects.filter(component_id=comp):
            review = {  'rating' : r.rating,
                        'comment' : r.comment,
                        'date' : str(r.date),
                        'user' : str(r.user)
            }
            reviews.append( review )

    except ObjectDoesNotExist:
        print 'Component has no reviews'

    return reviews

#
#
def getLoggedUserInfo(user):
    """
    getLoggedUserInfo(user) -> Return a dictionary filled with user information

    Fields:
        username
        country
        region
        city
    """

    uinfo = {}

    uinfo['username'] = user.username
    uinfo['id'] = user.id
    uinfo['groups'] = [g.name for g in user.groups.all()]

    try:
        userprofile = models.UserProfile.objects.get(pk=user)
        
        uinfo['country'] = userprofile.country
        uinfo['region'] = userprofile.region
        uinfo['city'] = userprofile.city

    except ObjectDoesNotExist:
        pass

    return uinfo


#
#
def createComponentReview(ref, user, form_rating, form_comment):
    """
    createComponentReview(ref, user, form_rating, form_comment) ->
        Creates a review instace associated to the specified component and user

    Throws ObjectDoesNotExist if the given reference does not exist
    """
    
    component = models.Component.objects.get(pk=ref)
    review = models.ComponentReview(rating=form_rating,
                                    comment=form_comment,
                                    component=component,
                                    user=user)
    review.save()