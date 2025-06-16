import connexion
from sqlalchemy.exc import OperationalError
from swagger_server.db.session import SessionLocalUsersDB
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_create import UserCreate  # noqa: E501
from swagger_server import util
from swagger_server.db.session import usersTable


def user_post(body):  # noqa: E501
    """Creates a user.

    Create a user. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: User
    """
    if connexion.request.is_json:

        sql = f"INSERT INTO {usersTable} (email, username, password) VALUES (:email, :username, :password)"

        try:
            db = SessionLocalUsersDB()
            db.execute(sql, {
                "email": body["email"],
                "username": body["username"],
                "password": body["password"]
            })
            data = UserCreate.from_dict(connexion.request.get_json())
            db.commit()
            db.close()
            return data, 201

        except OperationalError:
            return Error(code=503, message="Database not available"), 503


def user_user_id_get(user_id):  # noqa: E501
    #Get User by Id

    try:
        db = SessionLocalUsersDB()
        sql = f"SELECT email FROM {usersTable} WHERE id = :id"
        result = db.execute(sql, {"id": user_id}) 
        row = result.fetchone()
        db.close()

        if row is None: return Error(code=404, message="User not found"), 404

        user = User(email=row.email)
        return user, 200

    except OperationalError as e:
        return Error(code=503, message="Database not available"), 503
