from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from dashboard_auth.views import require_login

@require_login
def project(request):
    """project request"""
    request.session.get("username", None)
    return render(request, "project.html")
