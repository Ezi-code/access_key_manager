from django.test import TestCase
from accounts.models import User
from accounts.views import LoginView, RegisterView, ConfirmEmailView


class TestUserObject(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="user@demo.com",
            password="password",
            first_name="John",
            last_name="Doe",
        )
        assert user.email == "user@demo.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.is_active == True
        assert user.is_staff == False
        assert user.is_superuser == False
        assert user.is_registration_complete == False

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="superuser@demo.com",
            password="password",
            first_name="John",
            last_name="Doe",
        )
        assert user.email == "superuser@demo.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.is_active == True
        assert user.is_staff == True
        assert user.is_superuser == True
        assert user.is_registration_complete == True


class TestLoginView(TestCase):
    def test_get(self):
        request = self.client.get("/accounts/login/")
        assert request.status_code == 200

    def test_post(self):
        user = User.objects.create_user(
            email="test@demo.com",
            password="password",
        )
        response = self.client.post(
            "/accounts/login/",
            {
                "username": "test@demo.com",
                "password": "password",
            },
        )
        assert response.status_code == 200


class TestRegisterView(TestCase):
    def test_get(self):
        request = self.client.get("/accounts/register/")
        assert request.status_code == 200

    def test_post(self):
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "test",
                "email": "test@demo.com",
                "password": "password",
                "password1": "password",
            },
        )
        assert response.status_code == 302
