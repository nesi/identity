'''
Created on 21/08/2011

@author: yhal003
'''
try:
    import VOMSCommands
except ImportError:
    from VOMSAdmin import VOMSCommands

VOMS_CERTIFICATE="/home/yhal003/projects/certificates/test_cert.pem"
VOMS_KEY="/home/yhal003/projects/certificates/test_key.pem"
VOMS_VO="/nz"
VOMS_HOST="voms.bestgrid.org"
VOMS_PORT="8443"

class VomsConnector(object):
    '''
    used to connect to VOMS server
    '''


    def __init__(self):
        self.voms  = VOMSCommands.VOMSAdminProxy(host=VOMS_HOST,
                                                 port=VOMS_PORT,
                                                 user_cert=VOMS_CERTIFICATE,
                                                 user_key=VOMS_KEY,
                                                 vo=VOMS_VO);
    
    def listGroups(self, dn=None, ca=None):
        if (dn == None):
            return self.voms.admin.listGroups()
        else:
            try:
                return self.voms.admin.listUserGroups(dn, ca)
            except Exception:
                return []
    
        
