from faker import Factory
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

fake = Factory.create()


class BaseTestCase(APITestCase):
    """A base test case for User and Bucketlist test classes."""

    def setUp(self):
        """Run instructions before the each test is executed."""
        self.email = fake.email()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create(
            username=self.username, password=self.password, email=self.email)

    def tearDown(self):
        """Run instructions after each test is executed."""
        del self.user

