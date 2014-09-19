from keystoneclient.v3 import client as client_v3
from dashboard import settings
from django.utils import timezone

AUTH_URL = settings.AUTH_URL


def authenticate(request=None, username=None, password=None,
                 token=None,
                 project_id=None,
                 project_name=None,
                 user_domain_name=None, auth_url=AUTH_URL):
    """ authenticate  """
    message = "success"
    try:
        client = client_v3.Client(username=username,
                                  password=password,
                                  token=token,
                                  project_id=project_id,
                                  project_name=project_name,
                                  user_domain_name=user_domain_name,
                                  auth_url=auth_url,
                                  debug=settings.DEBUG)
    except Exception, e:
        print e.message
        message = e.message
        return {"result": False, "message": message}
    return {"result": True,
            "message": message,
            "client": client}


def authenticate_with_project(project_id=None,
                             token=None,
                             auth_url=AUTH_URL):
    """auth with tenant"""
    message = "success"
    try:
        client = client_v3.Client(project_id=project_id, token=token,
                                  auth_url=auth_url)
    except Exception, e:
        message = e.message
        return {"result": False, "message": message}
    return {"result": True, "message": message, "client": client}


def check_expiration(expires_at):
    expiration = expires_at
    if settings.USE_TZ and timezone.is_naive(expiration):
        expiration = timezone.make_aware(expiration, timezone.utc)
    if expiration:
        return expiration > timezone.now()
    else:
        return False
