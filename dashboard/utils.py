from django.core.urlresolvers import reverse

def get_default_panel_url():
    return reverse("project", args=('overview',))


def nova_create_server(request, client):
    """create a virtual server"""
    name = request.POST.get('inputServerName', None)
    flavor_id = request.POST.get('inputServerFlavor', None)
    #count = request.POST.get('inputServerCount', 0)
    #boot_type = request.POST.get('inputServerBootType', None)
    image_id = request.POST.get('inputServerImage', None)

    manager = client.servers


    try:
        server = manager.create(name, image_id, flavor_id)
        return {'result':True, 'server':server}
    except Exception, e:
        print e.message
        return {'result':False, 'message':e.message}
