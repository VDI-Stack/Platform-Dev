from novaclient.client import Client as nova_client


API_VERSION = 2


def get_nova_client(username,
                    password,
                    tenant_name,
                    auth_url):
    """get nova client and catch error"""
    try:
        client = nova_client(API_VERSION, username,
                             password, tenant_name,
                             auth_url)
        return {"result":True,
                "message":"success",
                "client":client}
    except Exception, e:
        return {"result":False,
                "message":e.message}