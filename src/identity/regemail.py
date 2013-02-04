'''
Created on 22/08/2011

@author: yhal003
'''
import smtplib
try:
    from email.mime.text import MIMEText
# support python 2.4
except ImportError:
    from email.MIMEText import MIMEText

class DummyMailSender(object):
    def __init__(self):
        pass
    
    def send(self,message):
        print message

class MailSender(object):
    '''
    sends emails to admins of the group
    '''

    def __init__(self):
        pass

    def send(self, message):
        send(self,message,"identity@auckland.ac.nz")

    def send(self,message,addr):
        msg = MIMEText(message)
        me = addr
        you = "eresearch@nesi.org.nz"
        msg["Subject"] = "Application for VO Membership"
        msg["To"] =  you
        msg["From"] = me
        s = smtplib.SMTP('localhost')
        s.sendmail(me, [you], msg.as_string())
        
