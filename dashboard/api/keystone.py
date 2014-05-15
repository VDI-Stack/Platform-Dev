from keystoneclient.v2_0 import client as client_v2

def get_tenant_list(auth_url, username, password):
    auth_url = auth_url
    tenant_list = []
    try:
        client = client_v2.Client(username=username,\
            password = password,\
            auth_url = auth_url,
            debug = True)
    except Exception,e:
        return tenant_list
    return client.tenants.list()
