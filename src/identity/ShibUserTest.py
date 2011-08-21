'''
Created on 20/08/2011

@author: yhal003
'''
import unittest
from identity.ShibUser import ShibUserException
from identity.ShibUser import SlcsUserNotFoundException
import identity.ShibUser as ShibUser


class ShibUserTest(unittest.TestCase):
    
    
    simpleACL = """
https://idp.canterbury.ac.nz/idp/shibboleth, /DC=nz/DC=org/DC=bestgrid/DC=slcs/O=University of Canterbury
"""

    complexACL = """
https://idp.canterbury.ac.nz/idp/shibboleth, /DC=nz/DC=org/DC=bestgrid/DC=slcs/O=University of Canterbury
https://idp.lincoln.ac.nz/idp/shibboleth, /DC=nz/DC=org/DC=bestgrid/DC=slcs/O=Lincoln University
https://idp.auckland.ac.nz/idp/shibboleth, /DC=nz/DC=org/DC=bestgrid/DC=slcs/O=The University of Auckland
"""

    nullACL = None

    canterburyDn = "/DC=nz/DC=org/DC=bestgrid/DC=slcs/O=University of Canterbury"
    canterburyIdp = "https://idp.canterbury.ac.nz/idp/shibboleth"
    aucklandDn = "/DC=nz/DC=org/DC=bestgrid/DC=slcs/O=The University of Auckland"
    aucklandIdp = "https://idp.auckland.ac.nz/idp/shibboleth"

    def testSimpleACL(self):
        cn = "First Second"
        token = "abc"
        dn = ShibUser.shib2dn(self.simpleACL, token = token, cn = cn, idp = self.canterburyIdp)
        self.assertEqual(dn, self.canterburyDn + "/CN=" + cn + " " + token)
        
    def testComplexACL(self):
        cn = "Name1 Name2"
        token = "xyz"
        dn = ShibUser.shib2dn(self.complexACL, cn = cn, token = token, idp = self.aucklandIdp)
        self.assertEqual(dn, self.aucklandDn + "/CN=" + cn + " " + token)
        
    def testNullACL(self):
        cn = "Name1 Name2"
        token = "xyz"
        self.assertRaises(ShibUserException, ShibUser.shib2dn, 
                          self.nullACL,cn, token,self.aucklandIdp)
    
    def testNullName(self):
        cn = None
        token = "xyz"
        self.assertRaises(ShibUserException, ShibUser.shib2dn, 
                          self.simpleACL,cn, token,self.aucklandIdp)
        
    def testNullToken(self):
        cn = "Name1 Name2"
        token = None
        self.assertRaises(ShibUserException, ShibUser.shib2dn, 
                          self.simpleACL,cn, token,self.aucklandIdp)
    
    def testNotFound(self):
        cn = "Name1 Name2"
        token = "xyz"
        self.assertRaises(SlcsUserNotFoundException, ShibUser.shib2dn, 
                          self.simpleACL,cn, token,self.aucklandIdp)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()