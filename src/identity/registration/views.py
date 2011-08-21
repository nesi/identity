# Create your views here.

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

import identity.settings as settings

def registration(request):
    auth = settings.getAuth(request)
    return render_to_response("registration/reg.html", {"auth": auth})