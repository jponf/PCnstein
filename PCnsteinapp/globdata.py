# -*- coding: utf-8 -*-

# Api entry url
API_URL = 'http://localhost:8000'

# Api components entry url
API_COMPONENTS = 'components'

# Api manufacturers entry url
API_MANUFACTURERS = 'manufacturers'

# Api categories entry url
API_CATEGORIES = 'categories'

# Api operating systems entry url
API_OS = 'os'

# Api element creation entry point
API_CREATE = 'create'

# Api element modification entry point
API_MODIFY = 'modify'

# Api create manufacturer url
API_CREATE_MANUFACTURER = '%s/%s' % (API_CREATE, API_MANUFACTURERS)

# Api create component url
API_CREATE_COMPONENT = '%s/%s' % (API_CREATE, API_COMPONENTS)

# Api modify manufacturer url
API_MODIFY_MANUFACTURER = '%s/%s' % (API_MODIFY, API_MANUFACTURERS)

# Api modify component url
API_MODIFY_COMPONENT = '%s/%s' % (API_MODIFY, API_COMPONENTS)