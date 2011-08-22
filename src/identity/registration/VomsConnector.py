'''
Created on 21/08/2011

@author: yhal003
'''
import VOMSCommands

class VomsConnector(object):
    '''
    used to connect to VOMS server
    '''


    def __init__(self):
        self.voms  = VOMSCommands.VOMSAdminProxy(host="voms.bestgrid.org",
                                                 port="8443",
                                                 user_cert="/home/yhal003/projects/certificates/test_cert.pem",
                                                 user_key="/home/yhal003/projects/certificates/test_key.pem",
                                                 vo="/nz");
    
    def listGroups(self, dn=None, ca=None):
        if (dn == None):
            return self.voms.admin.listGroups()
        else:
            return self.voms.admin.listUserGroups(dn, ca)
    
        