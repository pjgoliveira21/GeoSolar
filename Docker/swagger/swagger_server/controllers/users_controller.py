import connexion
from sqlalchemy.exc import OperationalError
from swagger_server.db.session import SessionLocalUsersDB
from swagger_server.models.error import Error 
from swagger_server.models.user import User
from swagger_server.models.response_user import ResponseUser
from swagger_server import util
from swagger_server.db.session import usersTable


def create_user(body):  # noqa: E501
    #Create a User
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400
    sql = f"INSERT INTO {usersTable} (email, username, password) VALUES (:email, :username, :password) RETURNING *"
    try:
        db = SessionLocalUsersDB()
        row = db.execute(sql, {
            "email": body["email"],
            "username": body["username"],
            "password": body["password"]
        }).fetchone()
        db.commit()
        db.close()
        return ResponseUser.from_dict(dict(row._mapping)), 201

    except OperationalError:
        return Error(code=503, message="Database not available"), 503

def delete_user_by_email(email):  # noqa: E501
    #delete a User by Email
    sql = f"DELETE FROM {usersTable} WHERE email = :email"
    try:
        db = SessionLocalUsersDB()
        db.execute(sql, {"email": email})
        db.commit()
        db.close()
        return None, 204
    except OperationalError:
        return Error(code=503, message="Database not available"), 503

def delete_user_by_id(user_id):  # noqa: E501
    # Delete User by Id
    sql = f"DELETE FROM {usersTable} WHERE id = :id"
    try:
        db = SessionLocalUsersDB()
        result = db.execute(sql, {"id": user_id})
        db.commit()
        db.close()

        if result.rowcount == 0: return Error(code=404, message="User not found"), 404

        return {}, 204

    except OperationalError:
        return Error(code=503, message="Database not available"), 503   

def get_all_users():  # noqa: E501
    # Get all Users
    try:
        db = SessionLocalUsersDB()
        sql = f"SELECT * FROM {usersTable}"
        result = db.execute(sql)
        rows = result.fetchall()
        db.close()

        users = []
        for row in rows:
            user = ResponseUser(**row._asdict())  # Convert row to dict and then to User model
            users.append(user)

        return users, 200
    except OperationalError as e:
        return Error(code=503, message="Database not available"), 503

def get_user_by_email(email):  # noqa: E501
    # Get User by Email
    try:
        db = SessionLocalUsersDB()
        sql = f"SELECT * FROM {usersTable} WHERE email = :email"
        result = db.execute(sql, {"email": email})
        row = result.fetchone()
        db.close()

        if row is None: return Error(code=404, message="User not found"), 404

        user = ResponseUser(**row._asdict())
        return user, 200
    except OperationalError as e:
        return Error(code=503, message="Database not available"), 503

def get_user_by_id(user_id):  # noqa: E501
    #get User by Id
    try:
        db = SessionLocalUsersDB()
        sql = f"SELECT * FROM {usersTable} WHERE id = :id"
        result = db.execute(sql, {"id": user_id}) 
        row = result.fetchone()
        db.close()

        if row is None: return Error(code=404, message="User not found"), 404

        user = ResponseUser(**row._asdict())
        return user, 200
    except OperationalError as e:
        return Error(code=503, message="Database not available"), 503

def patch_user_by_email(body, email):  # noqa: E501
    # Update User by Email
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400

    allowed_fields = {
        'email': 'email',
        'username': 'username',
        'password': 'password',
        'is_active': 'is_active',
        'last_login': 'last_login'
    }
    # Construir colunas e valores para o update só com os campos presentes no JSON
    columns = []
    values = {}
    data = connexion.request.get_json()
    for key, col_name in allowed_fields.items():
        if key in data and data[key] is not None:
            columns.append(f"{col_name} = :{col_name}")
            values[col_name] = data[key]

    if not columns: return Error(code=400, message="No valid fields provided for update"), 400

    sql = f"UPDATE {usersTable} SET {', '.join(columns)} WHERE email = :email RETURNING *"
    values['email'] = email

    try:
        db = SessionLocalUsersDB()
        row = db.execute(sql, values).fetchone()
        db.commit()
        db.close()
        return ResponseUser.from_dict(dict(row._mapping)), 201
    except OperationalError:
        return Error(code=503, message="Database not available"), 503

def patch_user_by_id(body, user_id):  # noqa: E501
    # Update User by Id
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400

    allowed_fields = {
        'email': 'email',
        'username': 'username',
        'password': 'password',
        'is_active': 'is_active',
        'last_login': 'last_login'
    }

    # Construir colunas e valores para o update só com os campos presentes no JSON
    columns = []
    values = {}
    data = connexion.request.get_json()

    for key, col_name in allowed_fields.items():
        if key in data and data[key] is not None:
            columns.append(f"{col_name} = :{col_name}")
            values[col_name] = data[key]

    if not columns: return Error(code=400, message="No valid fields provided for update"), 400

    sql = f"UPDATE {usersTable} SET {', '.join(columns)} WHERE id = :id RETURNING *"
    values['id'] = user_id

    try:
        db = SessionLocalUsersDB()
        row = db.execute(sql, values).fetchone()
        db.commit()
        db.close()
        return ResponseUser.from_dict(dict(row._mapping)), 201

    except OperationalError:
        return Error(code=503, message="Database not available"), 503

def update_user_by_email(body, email):  # noqa: E501
    # Update User by Email
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400
    data = connexion.request.get_json()
    allowed_fields = {
        'email': 'email',
        'username': 'username',
        'password': 'password',
        'is_active': 'is_active'
    }
    # Prepara o SQL para substituir todos os campos
    sql = f"""UPDATE {usersTable}
    SET email = :email,
        username = :username,
        password = :password,
        is_active = :is_active
    WHERE email = :email
    RETURNING *"""  

    values = {
        'email': data['email'],
        'username': data['username'],
        'password': data['password'],
        'is_active': data['is_active']
    }

    try:
        db = SessionLocalUsersDB()
        row = db.execute(sql, values).fetchone()
        db.commit()
        db.close()

        if row is None: return Error(code=404, message="User not found"), 404

        return ResponseUser.from_dict(dict(row._mapping)), 201
    except OperationalError:
        return Error(code=503, message="Database not available"), 503

def update_user_by_id(body, user_id):  # noqa: E501
    # Update User by Id
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400

    data = connexion.request.get_json()
    allowed_fields = {
        'email': 'email',
        'username': 'username',
        'password': 'password',
        'is_active': 'is_active'
    }
    # Prepara o SQL para substituir todos os campos
    sql = """    UPDATE users
    SET email = :email,
        username = :username,
        password = :password,
        is_active = :is_active
    WHERE id = :id
    RETURNING *"""

    values = {
        'email': data['email'],
        'username': data['username'],
        'password': data['password'],
        'is_active': data['is_active'],
        'id': user_id
    }
    try:
        db = SessionLocalUsersDB()
        row = db.execute(sql, values).fetchone()
        db.commit()
        db.close()

        if row is None: return Error(code=404, message="User not found"), 404

        return ResponseUser.from_dict(dict(row._mapping)), 201

    except OperationalError:
        return Error(code=503, message="Database not available"), 503
