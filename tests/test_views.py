from django.test import TestCase, Client
from faker import Factory
from django.core.urlresolvers import reverse
from django import forms
from api.forms import LoginForm, RegistrationForm

fake = Factory.create()


class TestViews(TestCase):
    """Test  functions."""

    def setUp(self):
        """initialize test resources."""
        self.client = Client()
        self.username = fake.user_name()
        self.email = fake.email()
        self.password = fake.password()

        # a user to perform requests that require authentication
        self.user = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        # create the user in the database
        self.client.post('/api/user/', data=self.user)

    def tearDown(self):
        """Free resources and do some housekeeping after tests are run."""
        del self.client
        del self.user

    def test_index_view(self):
        get_index = self.client.get('/')
        self.assertEqual(get_index.status_code, 200)
        self.assertTemplateUsed(get_index, 'index.html')

    def test_dashboard_view(self):
        url = reverse('dashboard')
        self.client.login(username=self.username, password=self.password)
        get_dashboard = self.client.get(url)
        self.assertEqual(get_dashboard.status_code, 302)

if __name__ == '__main__':
    unittest.main()