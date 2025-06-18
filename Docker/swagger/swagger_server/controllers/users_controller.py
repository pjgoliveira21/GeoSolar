import connexion
from sqlalchemy.exc import OperationalError
from swagger_server.db.session import SessionLocalUsersDB
from swagger_server.models.error import Error 
from swagger_server.models.user import User
from swagger_server.models.user_create import UserCreate
from swagger_server import util
from swagger_server.db.session import usersTable

def create_user(body):  # noqa: E501
    #Create a User
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400
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

def get_users():  # noqa: E501
    # Get all Users
    try:
        db = SessionLocalUsersDB()
        sql = f"SELECT * FROM {usersTable}"
        result = db.execute(sql)
        rows = result.fetchall()
        db.close()

        users = []
        for row in rows:
            user = User(**row._asdict())  # Convert row to dict and then to User model
            users.append(user)

        return users, 200
    except OperationalError as e:
        return Error(code=503, message="Database not available"), 503

def get_user_by_id(user_id):  # noqa: E501
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

def patch_user_by_id(body, user_id):  # noqa: E501
    # Update User by Id
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400

    allowed_fields = {
        'email': 'email',
        'username': 'username',
        'password': 'password'
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

    sql = f"UPDATE {usersTable} SET {', '.join(columns)} WHERE id = :id"
    values['id'] = user_id

    try:
        db = SessionLocalUsersDB()
        db.execute(sql, values)
        db.commit()
        db.close()
        return User.from_dict(connexion.request.get_json()), 200

    except OperationalError:
        return Error(code=503, message="Database not available"), 503

def update_user_by_id(body, user_id):  # noqa: E501
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400

    data = connexion.request.get_json()

    # Prepara o SQL para substituir todos os campos
    sql = """
    UPDATE users
    SET email = :email,
        username = :username,
        password = :password
    WHERE id = :id
    """

    values = {
        'email': data['email'],
        'username': data['username'],
        'password': data['password'],
        'id': user_id
    }

    try:
        db = SessionLocalUsersDB()
        result = db.execute(sql, values)
        db.commit()
        db.close()

        # Se não existia utilizador com esse id, pode ser bom verificar se houve update
        if result.rowcount == 0:
            return Error(code=404, message="User not found"), 404

        # Retorna o user atualizado
        return User.from_dict(data), 200

    except OperationalError:
        return Error(code=503, message="Database not available"), 503

def delete_user_by_id(user_id):
    # Delete User by Id
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400

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