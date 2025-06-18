# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.station import Station  # noqa: E501
from swagger_server.models.station_update import StationUpdate  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStationsController(BaseTestCase):
    """StationsController integration test stubs"""

    def test_create_station(self):
        """Test case for create_station

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

    def test_delete_station_by_id(self):
        """Test case for delete_station_by_id

        Delete Station by Id
        """
        response = self.client.open(
            '//station/{stationId}'.format(station_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_station_by_id(self):
        """Test case for get_station_by_id

        Get Station by Id
        """
        response = self.client.open(
            '//station/{stationId}'.format(station_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_stations(self):
        """Test case for get_stations

        Get all stations
        """
        query_string = [('offset', 0),
                        ('limit', 100),
                        ('search', 'search_example')]
        response = self.client.open(
            '//stations',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_station_by_id(self):
        """Test case for patch_station_by_id

        Partially update Station by Id
        """
        body = StationUpdate()
        response = self.client.open(
            '//station/{stationId}'.format(station_id=789),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_station_by_id(self):
        """Test case for update_station_by_id

        Fully update Station by Id
        """
        body = Station()
        response = self.client.open(
            '//station/{stationId}'.format(station_id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
