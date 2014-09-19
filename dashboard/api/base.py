

def url_for(catalog, service_type, endpoint_type="publicURL", region="regionOne"):
    service = get_service_from_catalog(catalog, service_type)
    if service:
        url = get_url_for_service(service,
                                  region,
                                  endpoint_type)
        if url:
            return url
    # raise exception
    return None


def is_service_enabled(catalog, service_type, service_name=None, region="regionOne"):
    service = get_service_from_catalog(catalog, service_type)

    if service:
        for endpoint in service['endpoints']:
            if service['type'] == 'identity' or \
                    endpoint['region'] == region:
                if service_name:
                    return service['name'] == service_name
                else:
                    return True


def get_service_from_catalog(catalog, service_type):
    if catalog:
        for service in catalog:
            if service['type'] == service_type:
                return service
    return None


def get_version_from_service(service):
    if service:
        endpoint = service['endpoints'][0]
        if 'interface' in endpoint:
            return 3
        else:
            return 2.0
    return 2.0


ENDPOINT_TYPE_TO_INTERFACE = {
    'publicURL': 'public',
    'internalURL': 'internal',
    'adminURL': 'admin',
}


def get_url_for_service(service, region, endpoint_type):
    identity_version = get_version_from_service(service)
    for endpoint in service['endpoints']:
        if service['type'] == 'identity' or region == endpoint['region']:
            try:
                if identity_version < 3:
                    return endpoint[endpoint_type]
                else:
                    interface = \
                        ENDPOINT_TYPE_TO_INTERFACE.get(endpoint_type, '')
                    if endpoint['interface'] == interface:
                        return endpoint['url']
            except (IndexError, KeyError):
                return None
    return None
