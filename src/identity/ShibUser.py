'''
Created on 20/08/2011

@author: yhal003
'''

class ShibUserException(Exception):
    def __init__(self, message):
        self.message = message
        

class SlcsUserNotFoundException(ShibUserException):
    def __init__(self, message):
        self.message = message

def shib2dn(acl, cn, token, idp):
    try:
        aclList = [a.split(",") for a in acl.split("\n")]
        iDn = ""
        for entry in aclList:
            if (idp == entry[0]):
                iDn = entry[1]
                break
    
        if (iDn.strip() == ""):
            raise SlcsUserNotFoundException("User Not Found")
    except AttributeError:
        raise ShibUserException("Parameters Cannot Be Null")
    
    return iDn.strip() + "/CN=" + cn + " " + token 

class ShibUser(object):
    '''
    classdocs
    '''


    def __init__(self, acl, cn, token):
        '''
        Constructor
        '''
        self.acl = acl
        self.cn = cn
        self.token = token
        
    
    
        