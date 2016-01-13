import os
from tests.test_base import BaseTestCase
from api.models import Bucketlist, Item


class TestBucketList(BaseTestCase):
    """Class to test bucketlists"""

    def test_bucketlist_creation_requires_valid_authentication(self):
        """Test the method to create a new bucket list requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Bucketlist table should contain a bucketlist called \
        `Success Bucketlist Name`
        """
        pass

    def test_duplicate_bucketlist_creation_fails(self):
        """Test creating a duplicate bucket list fails.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Bucketlist table should contain a bucketlist called
        `Success Bucketlist Name`
        """
        pass

    def test_get_bucketlists_requires_authentication(self):
        """Test the method to list created bucketlists requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. Since the SetUp function adds test bucketlists the \
        successful response should contain 1 or more items
        """
        pass

    def test_get_single_bucketlist_requires_authentication(self):
        """Test the method to get a bucketlist succeeds with authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be\
        returned.
        """
        pass

    def test_update_bucketlists_requires_authentication(self):
        """Test the method to update a bucketlist requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Bucketlist table should contain a bucketlist called \
        `Edited Bucketlist Name`
        """
        pass

    def test_del_bucketlists_requires_authentication(self):
        """Test the method to delete a bucketlist requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response and a \
        Deleted message should be returned. The Bucketlist table should contain one item less
        from the initial count defined in SetUp
        """
        pass

    def test_bucketlist_item_creation_requires_authentication(self):
        """Test the method to create a bucketlist item requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Item table should contain a bucket called `Success \
        Bucketlist Item Name`
        """
        pass

    def test_bucketlist_item_creation_fails_with_no_data(self):
        """Test the method to create a bucketlist item requires data.

        Even with an authentication token a 400 BAD REQUEST response should be
        returned if no data is provided. `name` is required.
        """
        pass

    def test_get_single_bucketlist_item_requires_authentication(self):
        """Test the method to get a bucketlist item succeeds with authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned."""
        pass

    def test_update_bucketlist_item_requires_authentication(self):
        """Test the method to update a bucketlist item requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Item table should contain a bucketlist item called \
        `Edited Bucketlist Item Name`
        """
        pass

    def test_del_bucketlist_item_requires_authentication(self):
        """Test the method to delete a bucketlist item requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response and a \
        Deleted message should be returned. The Item table should contain one \
        entry less from the count before deletion
        """
        pass

    def test_bucketlist_pagination(self):
        """Test bucketlist pagination.

        Querying all items should return a json result with 5 items. With a \
        limit only the number of items specified should be returned
        """
        pass

    def test_search_by_name(self):
        """Test bucketlist search.

        Specifying a search term should return bucketlists containing the \
        search term in their name
        """
        pass


if __name__ == '__main__':
    unittest.main()