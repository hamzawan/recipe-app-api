"""Test for the user API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return a user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()


    def test_create_user_success(self):
        payload = {
            "email": "test@example.com",
            "password": "pass123",
            "name": "Ameer Hamza"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn('password', res.data)


    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email" : "test@example.com",
            "password": "12345",
            "name": "Ameer Hamza"
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        """Test an error is returned if password is less then 5 chars."""

        payload = {
            "email":"test@example.com",
            "password": "pw",
            "name": "Ameer Hamza"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exist)


    def test_create_token_for_user(self):
        """Test generates token for valid user."""
        user_details = {
            'name': 'Test user',
            'email': 'test@example.com',
            'password': 'test-pass-123'
        }

        create_user(**user_details)

        payload = {
            'email' : user_details["email"],
            'password': user_details["password"]
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return error if invalid credentials."""

        user_details = {
            'email': 'test@example.com',
            'password': 'good-pass'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': 'bad-pass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_blank_password(self):
        """Test return error if password is blank."""

        user_details = {
            'email': 'test@example.com',
            'password': 'test123'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
