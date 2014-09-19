# -*- coding:utf-8 -*-
from dashboard_auth.views import require_login, require_permission

from django.http import HttpResponse

import json


@require_login
@require_permission("1")
def admin_create_project(request):
    if request.method is 'POST':
        result = {'result': 'failed', 'message': 'Unknown reason!'}
        return HttpResponse(json.dumps(result, ensure_ascii=False))
