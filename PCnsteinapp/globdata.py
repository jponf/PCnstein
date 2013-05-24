# -*- coding: utf-8 -*-

# Api entry url
API_URL = 'http://localhost:8000'

# Api components entry url
API_COMPONENTS = 'components'

# Api manufacturers entry url
API_MANUFACTURERS = 'manufacturers'

# Api categories entry url
API_CATEGORIES = 'categories'

# Api supportedby url
API_SUPPORTEDBY = 'supportedby'

# Api operating systems entry url
API_OS = 'os'

# Api element creation entry point
API_CREATE = 'create'

# Api element modification entry point
API_MODIFY = 'modify'

# Api element deletion entry point
API_DELETE = 'delete'

# Api create component url
API_CREATE_COMPONENT = '%s/%s' % (API_CREATE, API_COMPONENTS)

# Api modify component url
API_MODIFY_COMPONENT = '%s/%s' % (API_MODIFY, API_COMPONENTS)

# Api delete component url
API_DELETE_COMPONENT = '%s/%s' % (API_DELETE, API_COMPONENTS)

# Api create component review
API_CREATE_COMPONENT_REVIEW = '%s/review' % (API_CREATE)

API_ADD_SUPPORTEDBY = '%s/%s' % (API_CREATE, API_SUPPORTEDBY)

API_DELETE_SUPPORTEDBY = '%s/%s' % (API_DELETE, API_SUPPORTEDBY)