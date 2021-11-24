# Django Load Balancer Health Check

Aliveness check for Django that bypasses ALLOWED_HOSTS for the purposes of load balancers

## Purpose

When running on some app platforms and behind some load balancers, it is often the case that the host header is not set appropriately for health checks. When these platforms perform an HTTP health check without the proper host header an *error 400 bad request* will be returned by Django. This package provides a method to allow for for a simple "aliveness" health check that bypasses the `ALLOWED_HOSTS` protections. `ALLOWED_HOSTS` protection is bypassed only for the status aliveness check URL and not for any other requests.

This package is not an alternative to something like [django-health-check](https://github.com/KristianOellegaard/django-health-check), but is instead a better alternative than the TCP health check that is the default on many load balancers. The TCP health checks can only see if your uWSGI/Gunicorn/Uvicorn/etc server is alive, while this package ensures that requests are being properly routed to Django.

## How it works

This package works by returning an HTTP response from a middleware class before Django's common middleware performs the host check. The Django URL routing system is also bypassed since that happens "below" all middleware. During request processing, *django-lb-health-check* checks if the request is a *GET* request and matches `settings.ALIVENESS_URL`. If it is, a static plain text "200 OK" response is returned bypassing any other processing.


## Usage

Install *django-lb-health-check*

```shell
pip install django-lb-health-check
```

Add *lb_health_check* to your middleware. It **must** be above *django.middleware.common.CommonMiddleware* and should be below *django.middleware.security.SecurityMiddleware*, as high in the stack as possible to prevent any queries or unneeded code from running during a health check.

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'lb_health_check.middleware.AliveCheck', #  <- New middleware here
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

Set the URL you want to use for your aliveness check. Note that a GET request to this URL **will** shadow any other route you have defined through the Django URL mapper. Aliveness URL can be a string for a single health check URL or a list of strings if you want the aliveness check to run from multiple URLs. The multiple URL strategy is helpful if you are changing the URL of the endpoint by allowing both the old and new URLs to be checked.

```python
ALIVENESS_URL = "/health-check/"
```

Test your health check after starting your server:

```bash
curl localhost:8000/health-check/
OK
```

Note that the example app has *lb_health_check* in INSTALLED_APPS. This is only nessecary for testing purposes - the app does not use any Django models, admin, views, URL routing, or the like that would require it to be listed in INSTALLED_APPS.