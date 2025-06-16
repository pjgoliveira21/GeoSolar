import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_create import UserCreate  # noqa: E501
from swagger_server import util


def user_post(body):  # noqa: E501
    """Creates a user.

    Create a user. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: User
    """
    if connexion.request.is_json:
        body = UserCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def user_user_id_get(user_id):  # noqa: E501
    """Get User by Id

     # noqa: E501

    :param user_id: User id
    :type user_id: int

    :rtype: User
    """
    return 'do some magic!'
