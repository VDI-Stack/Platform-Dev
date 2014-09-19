# -*- coding: UTF-8 -*-
from novaclient.client import Client as nova_client
from glanceclient.client import Client as glance_client

from dashboard.api import base

API_VERSION = 3


def get_nova_client(username,
                    password,
                    tenant_name,
                    auth_url):
    """get nova client and catch error"""
    try:
        client = nova_client(API_VERSION, username,
                             password, tenant_name,
                             auth_url)
        return {"result": True,
                "message": "success",
                "client": client}
    except Exception, e:
        return {"result": False,
                "message": e.message}


class Server(object):
    def __init__(self, server, auth_ref, novaclient):
        self.novaclient = novaclient
        self.server = server
        self.auth_ref = auth_ref
        self.id = self.get_id()
        self.name = self.get_name()
        self.image_name = self.get_image_name()
        self.ips = self.get_ips()
        try:
            self.flavor = novaclient.flavors.get(server.flavor['id'])
        except Exception, e:
            print e.message
            self.flavor = None

    def get_id(self):
        return self.server.id

    def get_name(self):
        return self.server.name

    def get_image_name(self):
        # url = base.url_for(self.auth_ref['catalog'], 'image')
        url = base.url_for(self.auth_ref['serviceCatalog'], 'image')
        try:
            # c = glance_client('1', url, token=self.auth_ref['auth_token'])
            c = glance_client('1', url, token=self.auth_ref.auth_token)
            image = c.images.get(self.server.image['id'])
            return image.name
        except Exception, e:
            print e
            return ""

        return ""

    def get_ips(self):
        # neutron_enable = \
        #        base.is_service_enabled(self.auth_ref['catalog'], 'network')
        neutron_enable = \
            base.is_service_enabled(self.auth_ref['serviceCatalog'], 'network')
        ips = []
        if neutron_enable:
            # TODO: use neutron
            return "Use neutron "
        else:
            local_ips = self.server.addresses['private']
            for ip in local_ips:
                if ip['version'] == 4:
                    ips.append(ip['addr'])
        return ips

    def get_key_pair(self):
        return "keypair1"

    @property
    def flavor_name(self):
        if self.flavor:
            return self.flavor.name

    @property
    def vcpu(self):
        if self.flavor:
            return str(self.flavor.vcpus)+"虚拟内核"

    @property
    def vmem(self):
        if self.flavor:
            return str(self.flavor.ram)+"MB 内存"

    @property
    def vdisk(self):
        if self.flavor:
            return str(self.flavor.disk)+"bytes 盘"

    def get_vNIC(self):
        return "asdfadf"

    @property
    def status(self):
        return self.server.status

    @property
    def power_status(self):
        try:
            if self.server.__dict__["OS-EXT-STS:power_state"] == 1:
                return "On"
            else:
                return "Off"
        except Exception, e:
            pass
        try:
            if self.server.__dict__['os-extended-status:power_state']\
                    == 1:
                return "On"
            else:
                return "Off"
        except Exception, e:
            print e.message
            pass
        return "unknown"

    def start_time(self):
        try:
            starttime = self.server.__dict__["os-server-usage:launched_at"]
            if starttime:
                import datetime
                t = datetime.datetime.strptime(
                    starttime, "%Y-%m-%dT%H:%M:%S.%f")
                return t.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return "-"
        except Exception:
            pass
        try:
            starttime = self.server.__dict__["OS-SRV-USG:launched_at"]
            if starttime:
                import datetime
                t = datetime.datetime.strptime(
                    starttime, "%Y-%m-%dT%H:%M:%S.%f")
                return t.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return "-"
        except Exception, e:
            print e.message
            pass
        return "-"


