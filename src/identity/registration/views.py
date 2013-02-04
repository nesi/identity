# Create your views here.

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

import identity.auth as auth
import identity.registration.shib as shib
import identity.regemail as regemail
from identity.registration.voms import VomsConnector
from identity.registration.models import NeSIUser,Request, Project

from django import forms

class RequestForm(forms.Form):
    error_css_class = 'error'
    email = forms.EmailField(required=True, widget = forms.TextInput(attrs={'size': 40}))
    phone = forms.CharField(required=True,  widget = forms.TextInput(attrs={'size': 40}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':100})  ,required=True)
    groups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False)
    
def registration_resubmit(request):
    return registration(request, True)

# Maps the IDP to the VOMS group
def institution_mapping(provider):

	# CRIs:
	#
	# AgResearch: /nz/agresearch
	# ESR: /nz/esr
	# IRL: /nz/irl
	# Plant and Food: /nz/pfr
	# NIWA: /nz/niwa
	# GNS: /nz/gns
	# Scion: /nz/scion
	# Landcare: /nz/landare
	#
	# Universities:
	#
	# Auckland: /nz/uoa
	# Massey: /nz/massey
	# UC: /nz/bluefern
	# VUW: /nz/vuw
	# Otago: /nz/uoo
	# Waikato: /nz/waikato
	# Lincoln: /nz/lincoln 
	# AUT: /nz/aut
    
    mapping = {
            'http://iam.test.auckland.ac.nz/idp':'/nz/uoa',
            'http://iam.auckland.ac.nz/idp':'/nz/uoa',   
            'https://idp.auckland.ac.nz/idp/shibboleth':'/nz/uoa',  
            'https://idp.canterbury.ac.nz/idp/shibboleth':'/nz/bluefern',        
            'https://idp.landcareresearch.co.nz/idp/shibboleth':'/nz/landcare',  
            'https://idp.massey.ac.nz/idp/shibboleth':'/nz/massey', 
            'https://idp.lincoln.ac.nz/idp/shibboleth':'/nz/lincoln'
            }

    if provider in mapping:
        return mapping[provider]
    else:
        return '/nz/nesi'

# Selected (checked) by default
def in_default(group):

    default = ['/nz/nesi']
    for d in default:
        #if group.startswith(d):
        if group == d :
            return True
            break

    return False 

def in_ignore(group):
	
	ignore_list = ['/nz/nesi/projects', '/nz/uoa/test', '/nz/uoa/admin']
	for i in ignore_list:
		if group.startswith(i):
			return True
			break

	return False

def in_collaboration(group):
    
    collab = ['/nz/nesi', '/nz/bestgrid', '/nz/virtual-screening', '/nz/uoo', '/nz/agresearch', '/nz/esr', '/nz/irl', '/nz/pfr', '/nz/niwa', '/nz/gns', '/nz/scion', '/nz/landcare', '/nz/uoa', '/nz/massey', '/nz/bluefern', '/nz/bluefern', '/nz/vuw', '/nz/uoo', '/nz/waikato', '/nz/linclon', '/nz/aut']
    for c in collab:
        if group.startswith(c):
            return True
            break

    return False   

def registration(request, resubmit=False):
    try:
        a = auth.getAuth(request)
    except KeyError:
        return HttpResponse(status=403)
    form = RequestForm()
    if (a.username ==None or a.cn == None or a.provider == None or a.token == None):
        return HttpResponse(status=403)
    
    v = VomsConnector()
    groups = v.listGroups()
    
    try:
        userDN = shib.shib2dn(shib.getACL(), a.cn, a.token, a.provider)
        # create user if does not exist
        q = NeSIUser.objects.filter(username = a.username, provider= a.provider)
        if (q.count() < 1):
            u = NeSIUser(username=a.username, provider = a.provider, email = a.email, token = a.token)
            u.save()
        else:
            u = q[0]
    except shib.SlcsUserNotFoundException:
        return HttpResponse(status=403)
    
    userGroups = v.listGroups(userDN, shib.SLCS_CA)
    nonUserGroups = []
    defaultChoices = []
    for g in groups:
        try:
            userGroups.index(g)
        except ValueError:
            pq = Project.objects.filter(vo=g)
            inst = institution_mapping(a.provider)
            if ( in_ignore(g) or not ( g.startswith(inst) or (in_default(g)) or in_collaboration(g) ) ): 
                continue
            if (pq.count() > 0):
                nonUserGroups.append((g,pq[0].label))
                if (g == inst or in_default(g)):
                    defaultChoices.append(g)
            else:
                nonUserGroups.append((g,g))
    #nonUserGroups.sort(lambda a,b: cmp(a[0],b[0]))
    nonUserGroups.sort(key=lambda tuple: tuple[1])
    msgstr = ""
    if request.method == 'POST':
        form = RequestForm(request.POST)
    else:
        form = RequestForm(initial={"email": u.email, "message": msgstr})
    
    form.fields['groups'].choices = nonUserGroups
    form.fields['groups'].initial = defaultChoices

    requestSubmitted = False
    qr = Request.objects.filter(user=q[0])
    if (qr.count() > 1 and not resubmit ):
        r = qr[0]
        requestSubmitted = True
    elif ((qr.count() > 1) and resubmit):
        r = qr[0]
        r.delete()
        requestSubmitted = False
    elif request.method == 'POST':
        if (not form.is_valid()):
            pass
        else:
            m = form.cleaned_data["message"]
            groupsToApply = form.cleaned_data["groups"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            r = Request(user = q[0], message = m)
            message = "#assignee g.soudlenkov@auckland.ac.nz"
            message += "DN is " + userDN + "\n"
            message += "email is " + email + "\n"
            message += "phone is " + phone + "\n"
            message += "I would like to apply for the following groups: " + ",".join(groupsToApply) + "\n"
            message += request.POST["message"]
            regemail.MailSender().send(message)
            r.save()
            requestSubmitted = True
        
    return render_to_response("reg.html", 
                              {"dn": a.cn, 
                               "groups": nonUserGroups, 
                               "userGroups": userGroups,
                               "requestSubmitted": requestSubmitted,
                               "form": form})

def create_request(request):
    a = auth.getAuth(request)
    if (a.cn == None or a.provider == None or a.token == None):
        return HttpResponse(status=401)
    q = NeSIUser.objects.filter(username = a.username, provider= a.provider)
    if (q.count() < 1):
        return HttpResponse(status=401)
    else:
        u = q[0]
    r = Request(user = q[0].id, message = request.POST["message"])
    r.save()
    return render_to_response("request.html")
