"""Middleware for the LB health check"""

import logging
from typing import Set

from django.conf import settings
from django.http import HttpResponse

log = logging.getLogger(__name__)

class AliveCheck:
    def __init__(self, get_response):
        self.get_response = get_response
        self.urls: Set[str] = set()

        try:
            aliveness_setting = settings.ALIVENESS_URL
            if isinstance(aliveness_setting, str):
                self.urls.add(aliveness_setting)
            elif isinstance(aliveness_setting, (list, set)):
                # Coerce everything into a string for safety
                for item in aliveness_setting:
                    self.urls.add(str(item))
            else:
                log.warn("ALIVENESS_URL must be a str, list, or set")
                
        except AttributeError:
            log.warn("ALIVENESS_URL was not set, aliveness check disabled")

    def __call__(self, request):
        # Intercept health check URL calls so
        # they bypass the allowed hosts check
        if request.method == "GET" and request.path in self.urls:
            return HttpResponse("OK")

        # Process the request as normal if it isn't a health check
        return self.get_response(request)
