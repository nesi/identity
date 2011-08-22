'''
Created on 21/08/2011

@author: yhal003
'''

def getAuth(request):
    return Auth()

class Auth(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.provider = "https://idp.auckland.ac.nz/idp/shibboleth"
        self.cn = "Yuriy Halytskyy"
        self.username = "yhal003"
        self.token = "iibLJCBQh9f3BJQ-zIaI3uvl4Yc"
        self.email = "y.halytskyy@auckland.ac.nz"