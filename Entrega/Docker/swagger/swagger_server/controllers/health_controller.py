from swagger_server.db.session import SessionLocalStationsDB, SessionLocalUsersDB
import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util


def health_check():  # noqa: E501
    # Health check for the API
    return InlineResponse200(status="OK"), 200


def health_check_stations():  # noqa: E501
    # Health check for stations
    try:
        db = SessionLocalStationsDB()
        db.execute("SELECT 1;")
        db.close()
        return InlineResponse200(status="OK"),200
    except Exception as e:
        return InlineResponse200(status="ERROR"), 503


def health_check_users():  # noqa: E501
    # Health check for users
    try:
        db = SessionLocalUsersDB()
        db.execute("SELECT 1;")
        db.close()
        return InlineResponse200(status="OK"), 200
    except Exception as e:
        return InlineResponse200(status="ERROR"), 503
