import os
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from tests.test_base import BaseTestCase
from api.models import Bucketlist, Item


class TestEndpoints(BaseTestCase):
    """Class to test api endpoints"""

    def test_bucketlist_creation(self):
        """Test the method to create a new bucket list.

        If the user is unauthenticated a 403 FORBIDDEN response should be
        returned. With authentication a 201 CREATED response should be
        returned. The Bucketlist table should contain a bucketlist called
        `BL Name - With auth`
        """
        no_auth_data = {'name': 'BL Name - No auth'}
        with_auth_data = {'name': 'BL Name - With auth'}
        before_auth = self.client.post(self.bucketlists, no_auth_data)
        self.client.force_authenticate(self.user)
        after_auth = self.client.post(self.bucketlists, with_auth_data)
        self.assertEqual(before_auth.status_code, 403)
        self.assertEqual(after_auth.status_code, 201)
        self.assertEqual(after_auth.data['name'], 'BL Name - With auth')

    def test_bucketlist_retrieval(self):
        """Test listing bucketlists.

        If the user is unauthenticated a 403 FORBIDDEN response should be
        returned. With authentication a 200 OK response should be
        returned. The Bucketlist table should contain a bucketlist called
        `Initial Bucketlist` when queried by the first user
        """
        # Before authentication
        before_auth = self.client.get(self.bucketlists)

        # Force authentication
        self.client.force_authenticate(self.user)

        # After authentication
        all_bucketlists = self.client.get(self.bucketlists)
        single_bucketlist = self.client.get(self.bucketlist_detail)

        # Authenticate different user. The second user should only access
        # the bucketlists he owns
        self.client.force_authenticate(self.user_two)
        different_user = self.client.get(self.bucketlists)

        self.assertEqual(before_auth.status_code, 403)
        self.assertEqual(all_bucketlists.status_code, 200)
        self.assertEqual(single_bucketlist.status_code, 200)
        self.assertEqual(single_bucketlist.data['name'], 'Initial Bucketlist')
        self.assertGreater(all_bucketlists.data['count'], 0)
        self.assertEqual(different_user.data['count'], 0)

    def test_bucketlist_update(self):
        """Test the method to update a bucketlist.

        If the user is unauthenticated a 403 FORBIDDEN response should be
        returned. With authentication a 200 OK response should be
        returned. The Bucketlist table should contain a bucketlist called
        `Edited Bucketlist Name`
        """
        data = {'name': 'Edited Bucketlist Name - No auth'}
        before_auth = self.client.put(self.bucketlist_detail, data)
        self.client.force_authenticate(self.user)
        data = {'name': 'Edited Bucketlist Name'}
        edit_bucketlist = self.client.put(self.bucketlist_detail, data)
        response = self.client.get(self.bucketlist_detail)

        self.assertEqual(edit_bucketlist.status_code, 200)
        self.assertEqual(before_auth.status_code, 403)
        self.assertEqual(response.data['name'], 'Edited Bucketlist Name')

    def test_del_bucketlists(self):
        """Test the method to delete a bucketlist requires authentication.

        The Bucketlist table should contain one item less from the initial
        count.
        """
        self.client.force_authenticate(self.user)
        before_delete = self.client.get(self.bucketlists)
        count_before = before_delete.data['count']
        delete_bucketlist = self.client.delete(self.bucketlist_detail)
        single_after_delete = self.client.get(self.bucketlist_detail)
        after_delete = self.client.get(self.bucketlists)
        count_after = after_delete.data['count']

        self.assertEqual(single_after_delete.status_code, 404)
        self.assertGreater(count_before, count_after)
        self.assertEqual(count_before, count_after + 1)

    def test_adding_item(self):
        """Test the method to create a new bucket list item.

        Posting using the user who owns the bucketlist gives a 201 CREATED
        response. By a different user it results in a 400 BAD REQUEST
        """
        # Force authentication
        self.client.force_authenticate(self.user)
        data = {'bucketlist': self.initial_bucketlist.id, 'name': 'Item Name'}
        # After authentication
        add_item = self.client.post(self.items, data)

        # Authenticate different user.
        data = {'bucketlist': self.initial_bucketlist.id, 'name': 'Item Two'}
        self.client.force_authenticate(self.user_two)
        different_user = self.client.post(self.items, data)
        self.assertEqual(add_item.status_code, 201)
        self.assertEqual(different_user.status_code, 400)

    def test_item_retrieval(self):
        """Test getting a bucketlist items.

        If the user is unauthenticated a 403 FORBIDDEN response should be
        returned. With authentication a 200 OK response should be
        returned. The Items table should contain an item called
        `Initial Item`
        """
        # Before authentication
        before_auth = self.client.get(self.items)

        # Force authentication
        self.client.force_authenticate(user=self.user)

        # After authentication

        all_items = self.client.get(self.items)
        single_item = self.client.get(self.item_detail)

        self.assertEqual(before_auth.status_code, 403)
        self.assertEqual(all_items.status_code, 200)
        self.assertEqual(single_item.status_code, 200)
        self.assertEqual(single_item.data['name'], 'Initial Item')
        self.assertGreater(all_items.data['count'], 0)

    def test_item_update(self):
        """Test the method to update a bucketlist item.

        If the user is unauthenticated a 403 FORBIDDEN response should be
        returned. With authentication a 200 OK response should be
        returned. The Item table should contain a bucketlist item called
        `Edited Item Name`
        """
        data = {'name': 'Edited Item Name - No auth'}
        before_auth = self.client.put(self.item_detail, data)
        self.client.force_authenticate(self.user)
        data = {
            'name': 'Edited Item Name',
            'bucketlist': self.initial_bucketlist.id
        }
        edit_item = self.client.put(self.item_detail, data)
        # import ipdb; ipdb.set_trace()
        response = self.client.get(self.item_detail)

        self.assertEqual(edit_item.status_code, 200)
        self.assertEqual(before_auth.status_code, 403)
        self.assertEqual(response.data['name'], 'Edited Item Name')

    def test_del_item(self):
        """Test the method to delete a bucketlist item.

        The Item table should contain one item less
        from the initial count.
        """
        self.client.force_authenticate(self.user)
        before_delete = self.client.get(self.items)
        count_before = before_delete.data['count']
        delete_item = self.client.delete(self.item_detail)
        single_after_delete = self.client.get(self.item_detail)
        after_delete = self.client.get(self.items)
        count_after = after_delete.data['count']

        self.assertEqual(single_after_delete.status_code, 404)
        self.assertGreater(count_before, after_delete.data['count'])
        self.assertEqual(count_before, count_after + 1)

    # def test_adding_user(self):
    #     """Test the endpoint for adding/registering users.

    #     """
    #     data = {
    #         'email': 'user@email.com',
    #         'username': 'user',
    #         'password': 'password'
    #     }

    #     # self.assertIsInstance(user, User)
    #     before_add = self.client.get(self.users)
    #     count_before = before_add.data['count']

    #     add_user = self.client.post(self.users, data)
    #     user_detail = reverse('user-detail', kwargs={'pk': add_user.data['id']})
    #     added_user = self.client.get(user_detail)
    #     import ipdb; ipdb.set_trace()
    #     after_add = self.client.get(self.users)
    #     count_after = after_add.data['count']

    #     self.assertEqual(add_user.status_code, 201)

    #     self.assertLess(count_before, count_after)

if __name__ == '__main__':
    unittest.main()