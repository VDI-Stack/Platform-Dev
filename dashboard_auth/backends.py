from keystoneclient.v3 import client as client_v3
from django.utils import timezone
from django.conf import settings
from keystoneclient import exceptions as keystone_exceptions
from django.contrib.auth.models import AnonymousUser


class KeystoneBackend(object):
    """
    Django authentication backend class for use with
    ``django.contrib.auth``.
    """
    def authenticate(self, request=None, username=None, password=None,
                     token=None,
                     user_domain_name=None, auth_url=settings.AUTH_URL):
        insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
        ca_cert = getattr(settings, "OPENSTACK_SSL_CACERT", None)

        try:
            client = client_v3.Client(username=username,
                                      password=password,
                                      token=token,
                                      user_domain_name=user_domain_name,
                                      auth_url=auth_url,
                                      debug=settings.DEBUG)
        except (keystone_exceptions.Unauthorized,
                keystone_exceptions.Forbidden,
                keystone_exceptions.NotFound) as exc:
            msg = 'Invalid user name or password.'
            raise KeystoneAuthException(msg)
        except (keystone_exceptions.ClientException,
                keystone_exceptions.AuthorizationFailure) as exc:
            msg = 'An error occurred authenticating. Please try again later.'
            raise KeystoneAuthException(msg)

        return User(auth_ref=client.auth_ref)



class KeystoneAuthException(Exception):
    pass


class User(AnonymousUser):


    def __init__(self, auth_ref=None ):
        self.id = auth_ref.user_id
        self.pk = auth_ref.user_id
        self.username = auth_ref.user_name

    def __unicode__(self):
        return self.username
