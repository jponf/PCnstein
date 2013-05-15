# -*- coding: utf-8 -*-

#
#
def isUserInGroup(user, group_name):
    """
    isUserInGroup(user, group_name) -> Returns true if the user belongs to the
                                        specified groups
    """ 
    return user.groups.filter(name=group_name).count() > 0

