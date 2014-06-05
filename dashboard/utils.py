from django.core.urlresolvers import reverse

def get_default_panel_url():
    return reverse("project", args=('overview',))
