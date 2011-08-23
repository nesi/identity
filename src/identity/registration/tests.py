"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from identity.registration.models import Project,NeSIUser, Request
from identity.registration.shib import ShibUser,ShibException,shib2dn,SlcsUserNotFoundException
from identity.registration.views import RequestForm

import identity.auth

class BrokenAuth:
    def __init__(self):
        self.provider = None
        self.cn = None
        self.token = None
        self.email = None

class StaticAuth:
    def __init__(self):
        self.provider = "https://idp.auckland.ac.nz/idp/shibboleth"
        self.cn = "Yuriy Halytskyy"
        self.token = "iibLJCBQh9f3BJQ-zIaI3uvl4Yc"
        self.username = "yhal003"
        self.email = "y@halytskyy"
        
class WrongIDPAuth:
    def __init__(self):
        self.provider = "https://wrong-idp"
        self.cn = "Yuriy Halytskyy"
        self.token = "iibLJCBQh9f3BJQ-zIaI3uvl4Yc"
        self.username ="yhal003"
        self.email = "y@halytskyy"
    
class ShibTest(TestCase):
    
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
        dn = shib2dn(self.simpleACL, token = token, cn = cn, idp = self.canterburyIdp)
        self.assertEqual(dn, self.canterburyDn + "/CN=" + cn + " " + token)
        
    def testComplexACL(self):
        cn = "Name1 Name2"
        token = "xyz"
        dn = shib2dn(self.complexACL, cn = cn, token = token, idp = self.aucklandIdp)
        self.assertEqual(dn, self.aucklandDn + "/CN=" + cn + " " + token)
        
    def testNullACL(self):
        cn = "Name1 Name2"
        token = "xyz"
        self.assertRaises(ShibException, shib2dn, 
                          self.nullACL,cn, token,self.aucklandIdp)
    
    def testNullName(self):
        cn = None
        token = "xyz"
        self.assertRaises(ShibException, shib2dn, 
                          self.simpleACL,cn, token,self.aucklandIdp)
        
    def testNullToken(self):
        cn = "Name1 Name2"
        token = None
        self.assertRaises(ShibException, shib2dn, 
                          self.simpleACL,cn, token,self.aucklandIdp)
    
    def testNotFound(self):
        cn = "Name1 Name2"
        token = "xyz"
        self.assertRaises(SlcsUserNotFoundException, shib2dn, 
                          self.simpleACL,cn, token,self.aucklandIdp)
        
    
    def testViewRegStatic(self):
        client = Client()
        identity.auth.getAuth = lambda r: StaticAuth()
        response = client.get("/registration/")
        self.assertEqual(response.status_code,200)
    

    def testViewBrokenLogin(self):
        client = Client()
        identity.auth.getAuth = lambda r: BrokenAuth()
        response = client.get("/registration/")
        self.assertEqual(response.status_code,401)
        
    def testWrongIdpLogin(self):
        client = Client()
        identity.auth.getAuth = lambda r: WrongIDPAuth()
        response = client.get("/registration/")
        self.assertEqual(response.status_code,401)
    
    def testUserCreation(self):
        client = Client()
        sauth = StaticAuth()
        identity.auth.getAuth = lambda r: StaticAuth()
        # user does not exist before registration
        q = NeSIUser.objects.filter(username = sauth.username, provider= sauth.provider)
        self.assertEqual(q.count(), 0)
        response = client.get("/registration/")
        q = NeSIUser.objects.filter(username = sauth.username, provider= sauth.provider)
        self.assertEqual(q.count(), 1)
    
    def testCreateRequest(self):
        client = Client()
        sauth = StaticAuth()
        form = RequestForm()
        form.email = "y.halytskyy@gmail.com"
        form.message = "message"
        form.phone = "234234"
        message = "Please assign me to /ARCS/BeSTGIRD"
        identity.auth.getAuth = lambda r: StaticAuth()
        response = client.get("/registration/")
        q = NeSIUser.objects.filter(username = sauth.username, provider= sauth.provider)
        response = client.post("/registration/", {"message": form.message, "email": form.email, "phone": form.phone})
        q = Request.objects.filter(user = q[0])
        self.assertEqual(q.count(), 1)
        

class SimpleTest(TestCase):
    def setUp(self):
        u1 = NeSIUser(username="yhal003", 
                      token="abz",
                      provider="https://idp.auckland.ac.nz/idp/shibboleth",
                      email="y@email")
        u1.save()
        
    def tearDown(self):
        pass
        

