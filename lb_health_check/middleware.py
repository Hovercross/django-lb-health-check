"""Middleware for the LB health check"""

import logging
from typing import Set, Any

from django.conf import settings
from django.http import HttpResponse

log = logging.getLogger(__name__)

class AliveCheck:
    """A simple "am I responding to HTTP requests" check
    that is designed to be hit from a load balancer"""
    
    def __init__(self, get_response):
        self.get_response = get_response

        self.urls = _get_urls()
        
        if not self.urls:
            log.error("No aliveness URLs are defined, check disabled")

        for url in self.urls:
            log.info("Intercepting GET requests to %s for aliveness check", url)
            

    def __call__(self, request):
        # Intercept health check URL calls so
        # they bypass the allowed hosts check
        if request.method == "GET" and request.path in self.urls:
            return HttpResponse("OK\n")

        # Process the request as normal if it isn't a health check
        return self.get_response(request)

def _get_urls() -> Set[str]:
    try:
        val = settings.ALIVENESS_URL
    except AttributeError:
        log.warning("ALIVENESS_URL was not set")
        return set()

    if val is None:
        return set()

    if isinstance(val, str):
        return {val}
    
    if isinstance(val, (list, set)):
        out: Set[str] = set()

        for item in val:
            if not isinstance(item, str):
                log.warning("Item in ALIVENESS_URL was not a string: %s", item)
                continue
                
            out.add(item)
        
        return out
    
    log.warning("ALIVENESS_URL must be a str, list, or set. Got %s", val)
    return set()