from faker import Factory
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from api.models import Bucketlist, Item


fake = Factory.create()


class BaseTestCase(APITestCase):
    """A base test case for User and Bucketlist test classes."""

    def setUp(self):
        """Run instructions before the each test is executed."""
        self.email = fake.email()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create(
            username=fake.user_name(), password=fake.password(),
            email=fake.email()
        )

        self.initial_bucketlist = Bucketlist.objects.create(
            name='Initial Bucketlist', created_by=self.user)

        self.initial_item = Item.objects.create(
            name='Initial Item', bucketlist=self.initial_bucketlist)

        self.user_two = User.objects.create(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email()
        )

        self.users = reverse('user-list')

        self.bucketlists = reverse('bucketlist-list')

        self.bucketlist_detail = reverse(
            'bucketlist-detail', kwargs={'pk': self.initial_bucketlist.id})

        self.items = reverse(
            'bucketlist-items-list',
            kwargs={'parent_lookup_bucketlist': self.initial_bucketlist.id})

        self.item_detail = reverse(
            'bucketlist-items-detail',
            kwargs={
                'pk': self.initial_item.id,
                'parent_lookup_bucketlist': self.initial_bucketlist.id})

    def tearDown(self):
        """Run instructions after each test is executed."""
        del self.user
        del self.initial_bucketlist
        del self.initial_item

