from keystoneclient.v2_0 import client as client_v2
# from keystoneclient.v3 import client as client_v3

def authenticate(request=None, username=None, password=None,
    user_domain_name=None, auth_url=None):
    """ authenticate  """
    # TODO: add to settings
    auth_url = "http://192.168.2.10:5000/v2.0"
    message = "success"
    try:
        client = client_v2.Client(username=username,
                                  password=password,
                                  user_domain_name=user_domain_name,
                                  auth_url=auth_url,
                                  debug=True)
    except Exception, e:
        message = e.message
        return False, message
    return True,message

