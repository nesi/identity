'''
Created on 21/08/2011

@author: yhal003
'''
import VOMSCommands

class VomsConnector(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.voms  = VOMSCommands.VOMSAdminProxy(host="voms.bestgrid.org",
                                                 port="8443",
                                                 user_cert="/home/yhal003/projects/certificates/test_cert.pem",
                                                 user_key="/home/yhal003/projects/certificates/test_key.pem",
                                                 vo="/nz");
        
        