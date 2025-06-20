# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.base_station import BaseStation  # noqa: F401,E501
from swagger_server import util


class ResponseStation(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, country: str=None, continent: str=None, city: str=None, location_accuracy: str='approximate', latitude: float=None, longitude: float=None, name: str='Pulida Solar Park', capacity: float=None, capacity_rating: str='unknown', technology_type: str='unknown', status: str='operating', start_year: float=None, operator: str=None, owner: str=None, wiki_url: str=None, research_date: date=None, id: int=None, created_at: datetime=None, updated_at: datetime=None):  # noqa: E501
        """ResponseStation - a model defined in Swagger

        :param country: The country of this ResponseStation.  # noqa: E501
        :type country: str
        :param continent: The continent of this ResponseStation.  # noqa: E501
        :type continent: str
        :param city: The city of this ResponseStation.  # noqa: E501
        :type city: str
        :param location_accuracy: The location_accuracy of this ResponseStation.  # noqa: E501
        :type location_accuracy: str
        :param latitude: The latitude of this ResponseStation.  # noqa: E501
        :type latitude: float
        :param longitude: The longitude of this ResponseStation.  # noqa: E501
        :type longitude: float
        :param name: The name of this ResponseStation.  # noqa: E501
        :type name: str
        :param capacity: The capacity of this ResponseStation.  # noqa: E501
        :type capacity: float
        :param capacity_rating: The capacity_rating of this ResponseStation.  # noqa: E501
        :type capacity_rating: str
        :param technology_type: The technology_type of this ResponseStation.  # noqa: E501
        :type technology_type: str
        :param status: The status of this ResponseStation.  # noqa: E501
        :type status: str
        :param start_year: The start_year of this ResponseStation.  # noqa: E501
        :type start_year: float
        :param operator: The operator of this ResponseStation.  # noqa: E501
        :type operator: str
        :param owner: The owner of this ResponseStation.  # noqa: E501
        :type owner: str
        :param wiki_url: The wiki_url of this ResponseStation.  # noqa: E501
        :type wiki_url: str
        :param research_date: The research_date of this ResponseStation.  # noqa: E501
        :type research_date: date
        :param id: The id of this ResponseStation.  # noqa: E501
        :type id: int
        :param created_at: The created_at of this ResponseStation.  # noqa: E501
        :type created_at: datetime
        :param updated_at: The updated_at of this ResponseStation.  # noqa: E501
        :type updated_at: datetime
        """
        self.swagger_types = {
            'country': str,
            'continent': str,
            'city': str,
            'location_accuracy': str,
            'latitude': float,
            'longitude': float,
            'name': str,
            'capacity': float,
            'capacity_rating': str,
            'technology_type': str,
            'status': str,
            'start_year': float,
            'operator': str,
            'owner': str,
            'wiki_url': str,
            'research_date': date,
            'id': int,
            'created_at': datetime,
            'updated_at': datetime
        }

        self.attribute_map = {
            'country': 'country',
            'continent': 'continent',
            'city': 'city',
            'location_accuracy': 'locationAccuracy',
            'latitude': 'latitude',
            'longitude': 'longitude',
            'name': 'name',
            'capacity': 'capacity',
            'capacity_rating': 'capacityRating',
            'technology_type': 'technologyType',
            'status': 'status',
            'start_year': 'startYear',
            'operator': 'operator',
            'owner': 'owner',
            'wiki_url': 'wikiUrl',
            'research_date': 'researchDate',
            'id': 'id',
            'created_at': 'createdAt',
            'updated_at': 'updatedAt'
        }
        self._country = country
        self._continent = continent
        self._city = city
        self._location_accuracy = location_accuracy
        self._latitude = latitude
        self._longitude = longitude
        self._name = name
        self._capacity = capacity
        self._capacity_rating = capacity_rating
        self._technology_type = technology_type
        self._status = status
        self._start_year = start_year
        self._operator = operator
        self._owner = owner
        self._wiki_url = wiki_url
        self._research_date = research_date
        self._id = id
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def from_dict(cls, dikt) -> 'ResponseStation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The responseStation of this ResponseStation.  # noqa: E501
        :rtype: ResponseStation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def country(self) -> str:
        """Gets the country of this ResponseStation.


        :return: The country of this ResponseStation.
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country: str):
        """Sets the country of this ResponseStation.


        :param country: The country of this ResponseStation.
        :type country: str
        """

        self._country = country

    @property
    def continent(self) -> str:
        """Gets the continent of this ResponseStation.


        :return: The continent of this ResponseStation.
        :rtype: str
        """
        return self._continent

    @continent.setter
    def continent(self, continent: str):
        """Sets the continent of this ResponseStation.


        :param continent: The continent of this ResponseStation.
        :type continent: str
        """

        self._continent = continent

    @property
    def city(self) -> str:
        """Gets the city of this ResponseStation.


        :return: The city of this ResponseStation.
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city: str):
        """Sets the city of this ResponseStation.


        :param city: The city of this ResponseStation.
        :type city: str
        """

        self._city = city

    @property
    def location_accuracy(self) -> str:
        """Gets the location_accuracy of this ResponseStation.


        :return: The location_accuracy of this ResponseStation.
        :rtype: str
        """
        return self._location_accuracy

    @location_accuracy.setter
    def location_accuracy(self, location_accuracy: str):
        """Sets the location_accuracy of this ResponseStation.


        :param location_accuracy: The location_accuracy of this ResponseStation.
        :type location_accuracy: str
        """
        allowed_values = ["approximate", "exact"]  # noqa: E501
        if location_accuracy not in allowed_values:
            raise ValueError(
                "Invalid value for `location_accuracy` ({0}), must be one of {1}"
                .format(location_accuracy, allowed_values)
            )

        self._location_accuracy = location_accuracy

    @property
    def latitude(self) -> float:
        """Gets the latitude of this ResponseStation.


        :return: The latitude of this ResponseStation.
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: float):
        """Sets the latitude of this ResponseStation.


        :param latitude: The latitude of this ResponseStation.
        :type latitude: float
        """

        self._latitude = latitude

    @property
    def longitude(self) -> float:
        """Gets the longitude of this ResponseStation.


        :return: The longitude of this ResponseStation.
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: float):
        """Sets the longitude of this ResponseStation.


        :param longitude: The longitude of this ResponseStation.
        :type longitude: float
        """

        self._longitude = longitude

    @property
    def name(self) -> str:
        """Gets the name of this ResponseStation.


        :return: The name of this ResponseStation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this ResponseStation.


        :param name: The name of this ResponseStation.
        :type name: str
        """

        self._name = name

    @property
    def capacity(self) -> float:
        """Gets the capacity of this ResponseStation.


        :return: The capacity of this ResponseStation.
        :rtype: float
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity: float):
        """Sets the capacity of this ResponseStation.


        :param capacity: The capacity of this ResponseStation.
        :type capacity: float
        """

        self._capacity = capacity

    @property
    def capacity_rating(self) -> str:
        """Gets the capacity_rating of this ResponseStation.


        :return: The capacity_rating of this ResponseStation.
        :rtype: str
        """
        return self._capacity_rating

    @capacity_rating.setter
    def capacity_rating(self, capacity_rating: str):
        """Sets the capacity_rating of this ResponseStation.


        :param capacity_rating: The capacity_rating of this ResponseStation.
        :type capacity_rating: str
        """
        allowed_values = ["unknown", "MW/ac", "MWp/dc"]  # noqa: E501
        if capacity_rating not in allowed_values:
            raise ValueError(
                "Invalid value for `capacity_rating` ({0}), must be one of {1}"
                .format(capacity_rating, allowed_values)
            )

        self._capacity_rating = capacity_rating

    @property
    def technology_type(self) -> str:
        """Gets the technology_type of this ResponseStation.


        :return: The technology_type of this ResponseStation.
        :rtype: str
        """
        return self._technology_type

    @technology_type.setter
    def technology_type(self, technology_type: str):
        """Sets the technology_type of this ResponseStation.


        :param technology_type: The technology_type of this ResponseStation.
        :type technology_type: str
        """
        allowed_values = ["unknown", "PV", "Solar Thermal"]  # noqa: E501
        if technology_type not in allowed_values:
            raise ValueError(
                "Invalid value for `technology_type` ({0}), must be one of {1}"
                .format(technology_type, allowed_values)
            )

        self._technology_type = technology_type

    @property
    def status(self) -> str:
        """Gets the status of this ResponseStation.


        :return: The status of this ResponseStation.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this ResponseStation.


        :param status: The status of this ResponseStation.
        :type status: str
        """
        allowed_values = ["construction", "operating"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def start_year(self) -> float:
        """Gets the start_year of this ResponseStation.


        :return: The start_year of this ResponseStation.
        :rtype: float
        """
        return self._start_year

    @start_year.setter
    def start_year(self, start_year: float):
        """Sets the start_year of this ResponseStation.


        :param start_year: The start_year of this ResponseStation.
        :type start_year: float
        """

        self._start_year = start_year

    @property
    def operator(self) -> str:
        """Gets the operator of this ResponseStation.


        :return: The operator of this ResponseStation.
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator: str):
        """Sets the operator of this ResponseStation.


        :param operator: The operator of this ResponseStation.
        :type operator: str
        """

        self._operator = operator

    @property
    def owner(self) -> str:
        """Gets the owner of this ResponseStation.


        :return: The owner of this ResponseStation.
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner: str):
        """Sets the owner of this ResponseStation.


        :param owner: The owner of this ResponseStation.
        :type owner: str
        """

        self._owner = owner

    @property
    def wiki_url(self) -> str:
        """Gets the wiki_url of this ResponseStation.


        :return: The wiki_url of this ResponseStation.
        :rtype: str
        """
        return self._wiki_url

    @wiki_url.setter
    def wiki_url(self, wiki_url: str):
        """Sets the wiki_url of this ResponseStation.


        :param wiki_url: The wiki_url of this ResponseStation.
        :type wiki_url: str
        """

        self._wiki_url = wiki_url

    @property
    def research_date(self) -> date:
        """Gets the research_date of this ResponseStation.


        :return: The research_date of this ResponseStation.
        :rtype: date
        """
        return self._research_date

    @research_date.setter
    def research_date(self, research_date: date):
        """Sets the research_date of this ResponseStation.


        :param research_date: The research_date of this ResponseStation.
        :type research_date: date
        """

        self._research_date = research_date

    @property
    def id(self) -> int:
        """Gets the id of this ResponseStation.


        :return: The id of this ResponseStation.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this ResponseStation.


        :param id: The id of this ResponseStation.
        :type id: int
        """

        self._id = id

    @property
    def created_at(self) -> datetime:
        """Gets the created_at of this ResponseStation.


        :return: The created_at of this ResponseStation.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        """Sets the created_at of this ResponseStation.


        :param created_at: The created_at of this ResponseStation.
        :type created_at: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self) -> datetime:
        """Gets the updated_at of this ResponseStation.


        :return: The updated_at of this ResponseStation.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        """Sets the updated_at of this ResponseStation.


        :param updated_at: The updated_at of this ResponseStation.
        :type updated_at: datetime
        """

        self._updated_at = updated_at
