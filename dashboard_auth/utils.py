from keystoneclient.v2_0 import client as client_v2
# from keystoneclient.v3 import client as client_v3

# TODO: add to settings
AUTH_URL = "http://192.168.2.10:5000/v2.0"

def authenticate(request=None, username=None, password=None,
    user_domain_name=None, auth_url=AUTH_URL):
    """ authenticate  """
    message = "success"
    try:
        client = client_v2.Client(username=username,
                                  password=password,
                                  user_domain_name=user_domain_name,
                                  auth_url=auth_url,
                                  debug=True)
    except Exception, e:
        message = e.message
        return {"result":False, "message":message}
    return {"result":True, "message":message, "auth_ref":client.auth_ref}


def authenticate_with_tenant(tenant_id=None,
                             token=None,
                             auth_url=AUTH_URL):
    """auth with tenant"""
    message = "success"
    try:
        client = client_v2.Client(tenant_id=tenant_id, token=token,
                                  auth_url=auth_url)
    except Exception, e:
        message = e.message
        return {"result":False, "message":message}
    return {"result":True, "message":message, "client":client}

