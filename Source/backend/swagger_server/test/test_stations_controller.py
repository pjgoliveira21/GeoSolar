# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.station import Station  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStationsController(BaseTestCase):
    """StationsController integration test stubs"""

    def test_station_post(self):
        """Test case for station_post

        Creates a station.
        """
        body = Station()
        response = self.client.open(
            '//station',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_station_station_id_get(self):
        """Test case for station_station_id_get

        Get Station by Id
        """
        response = self.client.open(
            '//station/{stationId}'.format(station_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
