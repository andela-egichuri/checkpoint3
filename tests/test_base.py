from faker import Factory
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

factory = APIRequestFactory()
fake = Factory.create()


class BaseTestCase(APITestCase):
    """A base test case for User and Bucketlist test classes."""

    def setUp(self):
        """Run instructions before the each test is executed."""
        user_url = reverse('user-list')

    def tearDown(self):
        """Run instructions after each test is executed."""
        pass

