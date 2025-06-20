# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.test import BaseTestCase


class TestHealthController(BaseTestCase):
    """HealthController integration test stubs"""

    def test_health_check(self):
        """Test case for health_check

        Health check endpoint
        """
        response = self.client.open(
            '/api/v1//health',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_health_check_stations(self):
        """Test case for health_check_stations

        Health check for stations
        """
        response = self.client.open(
            '/api/v1//health/stations',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_health_check_users(self):
        """Test case for health_check_users

        Health check for users
        """
        response = self.client.open(
            '/api/v1//health/users',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
