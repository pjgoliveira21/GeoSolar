# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_create import UserCreate  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUsersController(BaseTestCase):
    """UsersController integration test stubs"""

    def test_user_post(self):
        """Test case for user_post

        Creates a user.
        """
        body = UserCreate()
        response = self.client.open(
            '//user',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_user_id_get(self):
        """Test case for user_user_id_get

        Get User by Id
        """
        response = self.client.open(
            '//user/{userId}'.format(user_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
