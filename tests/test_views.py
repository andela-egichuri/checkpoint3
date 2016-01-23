from django.test import TestCase, Client
from faker import Factory
from django.core.urlresolvers import reverse, resolve
from django import forms
from django.contrib.auth.models import User
from api.models import Bucketlist
from api.forms import LoginForm, RegistrationForm

fake = Factory.create()


class TestViews(TestCase):
    """Test  Views."""

    def setUp(self):
        """ Initialize test resources."""

        # a user to perform requests that require authentication
        self.user_details = {
            'username': fake.user_name(),
            'email': fake.email(),
            'password': fake.password()
        }

        # create the user in the database
        self.add_user = self.client.post(
            reverse('user-list'), data=self.user_details)
        self.user = User.objects.get(id=self.add_user.data['id'])

    def tearDown(self):
        """ Free resources and do some housekeeping after tests are run."""

        del self.client
        del self.user
        del self.user_details

    def test_index_view(self):
        """ Test the homepage view."""
        url = reverse('index')
        before_login = self.client.get(url)
        self.client.force_login(self.user)
        after_login = self.client.get(url)
        self.assertEqual(before_login.status_code, 200)
        self.assertTemplateUsed(before_login, 'index.html')
        self.assertContains(before_login, '<a href="#login">Login</a>')
        self.assertEqual(after_login.status_code, 302)
        self.assertEqual(before_login.request['PATH_INFO'], '/')

    def test_dashboard_view(self):
        """ Test the dashboard view (Restricted)"""
        before_login = self.client.get(reverse('dashboard'))
        self.client.force_login(self.user)
        after_login = self.client.get(reverse('dashboard'))
        self.assertEqual(before_login.status_code, 302)
        self.assertEqual(after_login.status_code, 200)

    def test_login_in_index_view(self):
        """ Test the login feature on the homepage."""
        self.user_details['src'] = 'login'
        url = reverse('index')
        missing_data = self.client.post(url, {'src': 'login'})
        test_login = self.client.post(url, self.user_details)
        self.assertEqual(test_login.url, '/dashboard/')
        self.assertEqual(test_login.status_code, 302)
        self.assertContains(missing_data, 'field is required')

    def test_registration_in_index_view(self):
        """ Test the registration feature on the homepage."""
        password = fake.password()
        data = {
            'username': fake.user_name(),
            'email': fake.email(),
            'password': password,
            'conf_password': password,
            'src': 'reg'
        }
        url = reverse('index')
        test_reg = self.client.post(url, data)

        # Test with same email address but different username
        data['username'] = fake.user_name()
        reg_duplicate = self.client.post(url, data)

        # Test with password mismatch
        data['password'] = 'password'
        reg_password_mismatch = self.client.post(url, data)

        self.assertContains(test_reg, 'Registration complete.')
        self.assertContains(reg_duplicate, 'Email address taken')
        self.assertContains(reg_password_mismatch, 'The two password fields')
        self.assertEqual(test_reg.status_code, 200)

    def test_bucketlist_view(self):
        """ Test the single bucketlist view."""
        bucketlist = Bucketlist.objects.create(
            name='Initial Bucketlist', created_by=self.user)
        before_login = self.client.get('/bucketlists/' + str(bucketlist.id) + '/')
        self.client.force_login(self.user)
        after_login = self.client.get('/bucketlists/' + str(bucketlist.id) + '/')
        self.assertEqual(before_login.status_code, 302)
        self.assertEqual(after_login.status_code, 200)

    def test_api_view(self):
        """ Test the api browsable view."""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """ Test the logout view."""
        before_login = self.client.get('/logout/')
        self.client.force_login(self.user)
        logged_in = self.client.get('/logout/')
        self.assertEqual(before_login.status_code, 302)
        self.assertEqual(logged_in.status_code, 302)
        self.assertEqual(logged_in.url, '/')

if __name__ == '__main__':
    unittest.main()