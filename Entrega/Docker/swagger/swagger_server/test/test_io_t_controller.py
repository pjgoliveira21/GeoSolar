# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestIoTController(BaseTestCase):
    """IoTController integration test stubs"""

    def test_get_iot_data(self):
        """Test case for get_iot_data

        Get IoT data
        """
        response = self.client.open(
            '/api/v1//iot/{iotId}'.format(iot_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
