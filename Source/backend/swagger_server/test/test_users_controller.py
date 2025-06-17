# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_create import UserCreate  # noqa: E501
from swagger_server.models.user_user_id_body import UserUserIdBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUsersController(BaseTestCase):
    """UsersController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user

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

    def test_delete_user_by_id(self):
        """Test case for delete_user_by_id

        Delete User by Id
        """
        response = self.client.open(
            '//user/{userId}'.format(user_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_by_id(self):
        """Test case for get_user_by_id

        Get User by Id
        """
        response = self.client.open(
            '//user/{userId}'.format(user_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_users(self):
        """Test case for get_users

        Get all users
        """
        response = self.client.open(
            '//users',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_user_by_id(self):
        """Test case for patch_user_by_id

        Partially update User by Id
        """
        body = UserUserIdBody()
        response = self.client.open(
            '//user/{userId}'.format(user_id=789),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_user_by_id(self):
        """Test case for update_user_by_id

        Update User by Id
        """
        body = UserCreate()
        response = self.client.open(
            '//user/{userId}'.format(user_id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
