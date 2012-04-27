'''
Created on 21/08/2011

@author: yhal003

functions and classes to deal with SLCS
'''

import urllib2

SLCS_CA = "/DC=au/DC=org/DC=arcs/CN=ARCS SLCS CA 1"

class ShibException(Exception):
    def __init__(self, message):
        self.message = message
        

class SlcsUserNotFoundException(ShibException):
    def __init__(self, message):
        self.message = message
        
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
        
def getACL():
    return urllib2.urlopen("https://slcs1.arcs.org.au/idp-acl.txt").read()

'''
    generate user DN given SLCS acl string, user common name,
    token and IdP
'''
def shib2dn(acl, cn, token, idp):
    try:
        aclList = [a.split(",") for a in acl.split("\n")]
        iDn = ""
        for entry in aclList:
            if (idp == entry[0]):
                iDn = entry[1]
                break
''' hack for UoA IdP mapping '''
        if (idp.find("iam.auckland.ac.nz/idp") > -1):
            iDn = "/DC=nz/DC=org/DC=bestgrid/DC=slcs/O=The University of Auckland"

        if (iDn.strip() == ""):
            raise SlcsUserNotFoundException("User Not Found")
    except AttributeError:
        raise ShibException("Parameters Cannot Be Null")
    
    return iDn.strip() + "/CN=" + cn + " " + token 

