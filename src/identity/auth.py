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
        try:
            self.email = request.META["mail"]
        except KeyError:
            # don't need email
            self.email = ""
            pass
            


class Auth2(object):
    def __init__(self):
        self.provider ="https://idp.auckland.ac.nz/idp/shibboleth"
        self.cn = "Nick Jones"
        self.username = "njon001@auckland.ac.nz"
        self.token = "Y7rpGFpSV8z7TRK288wcQo9Eo_M"
        self.email = "njon001@aucklanduni.ac.nz"
        
class Auth3(object):
    def __init__(self):
        self.provider ="https://idp.auckland.ac.nz/idp/shibboleth"
        self.cn = "Random Person"
        self.username = "njon001@auckland.ac.nz"
        self.token = "tamparamtamparam"
        self.email = "njon001@aucklanduni.ac.nz"



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
