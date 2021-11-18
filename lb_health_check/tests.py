from django.test import TestCase, override_settings
from django.conf import settings

class AlivenessURLTestCase(TestCase):

    @override_settings(ALIVENESS_URL="/health-check/")
    def test_str(self):
        response = self.client.get("/health-check/")
        self.assertEqual(response.status_code, 200)
    
    @override_settings(ALIVENESS_URL={"/health-check/"})
    def test_set(self):
        response = self.client.get("/health-check/")
        self.assertEqual(response.status_code, 200)
    
    @override_settings(ALIVENESS_URL=["/health-check/"])
    def test_list(self):
        response = self.client.get("/health-check/")
        self.assertEqual(response.status_code, 200)
    
    @override_settings(ALIVENESS_URL=None)
    def test_none(self):
        with self.assertLogs(logger='lb_health_check.middleware', level='INFO') as cm:
            response = self.client.get("/health-check/")
            self.assertEqual(response.status_code, 404)

        self.assertIn("ERROR:lb_health_check.middleware:No aliveness URLs are defined, check disabled", cm.output)

    @override_settings()
    def test_missing(self):
        del settings.ALIVENESS_URL

        with self.assertLogs(logger='lb_health_check.middleware', level='INFO') as cm:
            response = self.client.get("/health-check/")
            self.assertEqual(response.status_code, 404)

        self.assertIn("WARNING:lb_health_check.middleware:ALIVENESS_URL was not set", cm.output)
        self.assertIn("ERROR:lb_health_check.middleware:No aliveness URLs are defined, check disabled", cm.output)

    @override_settings(ALIVENESS_URL="/health-check/")
    def test_other_url(self):
        response = self.client.get("/i-like-pie/")
        self.assertEqual(response.status_code, 404)
    
    @override_settings(ALIVENESS_URL=15)
    def test_non_string(self):
        with self.assertLogs(logger='lb_health_check.middleware', level='INFO') as cm:
            response = self.client.get("/health-check/")
            self.assertEqual(response.status_code, 404)
        
        self.assertIn("WARNING:lb_health_check.middleware:ALIVENESS_URL must be a str, list, or set. Got 15", cm.output)

    @override_settings(ALIVENESS_URL={15})
    def test_non_string_in_set(self):
        with self.assertLogs(logger='lb_health_check.middleware', level='INFO') as cm:
            response = self.client.get("/health-check/")
            self.assertEqual(response.status_code, 404)
        
        self.assertIn("WARNING:lb_health_check.middleware:Item in ALIVENESS_URL was not a string: 15", cm.output)