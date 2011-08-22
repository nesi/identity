'''
Created on 21/08/2011

@author: yhal003
'''

def getAuth(request):
    return Auth()

class ShibAuth(object):
    def __init__(self, request):
        self.token = request.META["shared-token"]
        self.provider = request.META["Shib-Identity-Provider"]
        self.cn = request.META["cn"]
        self.username = request.META["REMOTE_USER"]
        self.email = request.META["mail"]


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