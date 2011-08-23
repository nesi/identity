# Create your views here.

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

import identity.auth as auth
import identity.registration.shib as shib
import identity.regemail as email
from identity.registration.voms import VomsConnector
from identity.registration.models import NeSIUser,Request, Project

from django import forms

class RequestForm(forms.Form):
    error_css_class = 'error'
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, label="Message to BeSTGRID Demiurges",required=True)
    
def registration_resubmit(request):
    return registration(request, True)

def registration(request, resubmit=False):
    a = auth.getAuth(request)
    form = RequestForm()
    print a.cn
    if (a.cn == None or a.provider == None or a.token == None):
        return HttpResponse(status=401)
    
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
        return HttpResponse(status=401)
    
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
        form = RequestForm(request.POST)
        if (not form.is_valid()):
            pass
        else:
            r = Request(user = q[0], message = request.POST["message"])
            groupsToApply =  request.POST.getlist("apply_group")
            message = "DN is " + userDN + "\n"
            message += "email is " + request.POST["email"] + "\n"
            message += "phone is " + request.POST["phone"] + "\n"
            message += "I would like to apply for the following groups: " + ",".join([x[0] for x in groupsToApply]) + "\n"
            message += request.POST["message"]
            email.MailSender().send(message)
            r.save()
            requestSubmitted = True
        
    userGroups = v.listGroups(userDN, shib.SLCS_CA)
    
    nonUserGroups = []
    for g in groups:
        try:
            userGroups.index(g)
        except ValueError:
            pq = Project.objects.filter(vo=g)
            if ( not (g.startswith("/nz/uoa/") or (g.startswith("/nz/virtual-screening")))):
                continue
            if (pq.count() > 0):
                nonUserGroups.append((g,pq[0].label))
            else:
                nonUserGroups.append((g,g))
    nonUserGroups.sort(lambda a,b: cmp(a[0],b[0]))
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