# Django Load Balancer Health Check

Aliveness check for Django that bypasses ALLOWED_HOSTS

## Purpose

When running on app platforms (Heroku/DigitalOcean/etc), Kubernetes, AWS behind an Elastic Load Balancer, and other similar platforms it is often the case that the host header is not set appropriately for health checks. When these platforms perform an HTTP health check without the proper host header an *error 400 bad request* will be returned by Django. This is because the Django Common Middleware tests the host header and raises a DisalowedHost exception if it doesn't match what is in ALLOWED_HOSTS. This package provides an alternative health/aliveness check that is returned by middlware and thus bypasses the ALLOWED_HOSTS check. In order to accomplish this, django-lb-health-check middleware checks if the incoming URL is for the known health check URL and returns a response - bypassing the majority of the Django platform. It is not designed as a replacement for something like [django-health-check](https://github.com/KristianOellegaard/django-health-check), but instead as a better alternative to a TCP based aliveness check that ensures your Django project has been started and is responding to HTTP instead of just having a port open.

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
