from django.test import TestCase

from lb_health_check.middleware import AliveCheck

class AlivenessURLTestCase(TestCase):
    def test_str(self):
        with self.settings(ALIVENESS_URL="/health-check/"):
            response = self.client.get("/health-check/")
            self.assertEqual(response.status_code, 200)

    def test_set(self):
        with self.settings(ALIVENESS_URL={"/health-check/"}):
            response = self.client.get("/health-check/")
            self.assertEqual(response.status_code, 200)
    
    def test_list(self):
        with self.settings(ALIVENESS_URL=["/health-check/"]):
            response = self.client.get("/health-check/")
            self.assertEqual(response.status_code, 200)
    
    def test_none(self):
        # TODO: Figure out how to suppress the warning, since it's coming from
        # the middleware init and not the function call itself
        with self.settings(ALIVENESS_URL=None):
            response = self.client.get("/health-check/")
            self.assertEqual(response.status_code, 404)
    
    def test_other_url(self):
        with self.settings(ALIVENESS_URL="/health-check/"):
            response = self.client.get("/i-like-pie/")
            self.assertEqual(response.status_code, 404)