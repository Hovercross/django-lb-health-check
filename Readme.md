# Django Load Balancer Health Check

## Purpose

When running on app platforms (Heroku/DigitalOcean/etc), Kubernetes, and other similar platforms it is often the case that the host header is not set appropriately. On these platforms, a 400 bad request will be sent by the Django Common Middleware will raise a DisallowedHost exception. This package provides an alternative health check that is returned by middlware and thus bypasses the ALLOWED_HOSTS check. In order to accomplish this, the middleware checks if the incoming URL is for the known health check URL and returns a response without processing any additional middleware - thus bypassing the ALLOWED_HOSTS check for a single URL (or small list of URLs) only.

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

Set the URL you want to use for your aliveness check. Note that a GET request to this URL **will** shadow any other URL you have defined through the Django URL mapper. Aliveness URL can be a string for a single health check URL or a list of strings if you want the aliveness check to run from multiple URLs. The multiple URL strategy is helpful if you are changing the URL of the endpoint by allowing both the old and new URLs to be checked.

```python
ALIVENESS_URL = "/health-check/"
```

Test your health check after starting your server:

```bash
curl localhost:8000/health-check/
OK
```
