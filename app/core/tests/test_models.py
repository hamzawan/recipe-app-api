"""
Test for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""


    def test_create_user_with_email_successful(self):
        """Test create user with email successful"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test2@Example.com', 'test2@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, '12345')
            self.assertEqual(user.email, expected)

    def test_create_superuser(self):
        """Test to create a super user."""

        email = "admin@test.com"
        password = "123456"

        user = get_user_model().objects.create_superuser(
            email,
            password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)