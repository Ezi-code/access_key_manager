from django.test import TestCase


class TestAccountsDetails(TestCase):
    def test_get(self):
        request = self.client.get("/api/accounts-details/")
        assert request.status_code == 400
        assert request.json() == {"detail": "Email not provided"}


class TestAccountsDetailsWithEmail(TestCase):
    def test_get(self):
        request = self.client.get("/api/accouts-details/?email=root@demo.com")
        assert request.status_code == 404
