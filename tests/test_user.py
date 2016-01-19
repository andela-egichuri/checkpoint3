from tests.test_base import BaseTestCase


class TestUser(BaseTestCase):
    """Test user functions."""

    def test_user_can_log_in(self):
        """Test login success.

        With correct login credentials a token should be returned and set the
        user online status as True.
        """
        import ipdb; ipdb.set_trace()

    def test_wrong_login_credentials_fails(self):
        """Test login failure with wrong credentials.

        With wrong login credentials a token should not be returned. A `Login
        Failed` message should be returned
        """
        pass

    def test_user_creation_required_fields(self):
        """Test registration failure with no data provided.

        To create a user a username, password and email address are required.
        Omitting any of them raises a BAD REQUEST error
        """
        pass

    def test_user_creation_unique_fields(self):
        """Test registration failure with no data provided.

        To create a user a username, password and email address are required
        """
        pass

    def test_user_can_log_out(self):
        """Test logout success.

        On logout a `logged out` message should be returned and the user online
        status as False.
        """
        pass

if __name__ == '__main__':
    unittest.main()