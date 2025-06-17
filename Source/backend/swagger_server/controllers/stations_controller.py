import connexion
from sqlalchemy.exc import OperationalError
from swagger_server.db.session import SessionLocalStationsDB
from swagger_server.models.error import Error  # modelo gerado
from swagger_server.models.station import Station  # modelo gerado (Swagger)
from swagger_server.db.session import stationsTable


def create_station(body):  # noqa: E501
    """Creates a station."""
    if connexion.request.is_json:
        # Campos que vamos aceitar, obrigatórios + opcionais do schema
    
        allowed_fields = {
            'capacity': 'capacity',
            'name': 'name',
            'latitude': 'latitude',
            'longitude': 'longitude',
            'id': 'id',
            'country': 'country',
            'continent': 'continent',
            'city': 'city',
            'locationAccuracy': 'locationAccuracy',
            'capacityRating': 'capacityRating',
            'technologyType': 'technologyType',
            'status': 'status',
            'startYear': 'startYear',
            'operator': 'operator',
            'owner': 'owner',
            'wikiUrl': 'wikiUrl',
            'researchDate': 'researchDate'
        }

        # Construir colunas e valores para o insert só com os campos presentes no JSON
        columns = []
        placeholders = []
        values = {}
        data = connexion.request.get_json()

        for key, col_name in allowed_fields.items():
            if key in data and data[key] is not None:
                columns.append(col_name)
                placeholders.append(f":{col_name}")
                values[col_name] = data[key]

        # columns = ['name', 'latitude', 'longitude', 'capacity', 'country', ...]
        # placeholders = [':name', ':latitude', ':longitude', ':capacity', ':country', ...]
        # values = {'name': ..., 'latitude': ..., 'capacity': ..., 'country': ...}

        sql = f"INSERT INTO {stationsTable} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"

        try:
            db = SessionLocalStationsDB()
            db.execute(sql, values)
            db.commit()
            db.close()
            data = Station.from_dict(connexion.request.get_json())
            return data, 201

        except OperationalError:
            return Error(code=503, message="Database not available"), 503

    return Error(code=400, message="Invalid input"), 400

def get_stations(offset=0, limit=0):
    try:
        db = SessionLocalStationsDB()
        if(limit == 0):
            # If no limit is specified, we can use a default value or fetch all
            sql = f"SELECT * FROM {stationsTable} OFFSET :offset"
            result = db.execute(sql, {'offset': offset})
        else:
            sql = f"SELECT * FROM {stationsTable} LIMIT :limit OFFSET :offset"
            result = db.execute(sql, {'limit': limit, 'offset': offset})

        rows = result.fetchall()
        db.close()
        stations = [Station(**row._asdict()) for row in rows]
        return stations, 200

    except OperationalError:
        return Error(code=503, message="Database not available"), 500
    except Exception as e:
        return Error(code=500, message=f"Unexpected error: {e}"), 500
    
def get_station_by_id(station_id):  # noqa: E501
    """Get Station by Id"""
    try:
        db = SessionLocalStationsDB()
        sql = f"SELECT id, country, continent, city FROM {stationsTable} WHERE id = :id"
        result = db.execute(sql, {"id": station_id}) 
        row = result.fetchone()
        db.close()

        if row is None: return Error(code=404, message="Station not found"), 404

        station = Station(id=row.id,country=row.country, continent=row.continent, city=row.city)
        return station, 200

    except OperationalError as e:
        return Error(code=503, message="Database not available"), 503

def patch_station_by_id(body, station_id):  # noqa: E501
    # Update Station by Id
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400
    data = connexion.request.get_json()
    # Campos que vamos aceitar, obrigatórios + opcionais do schema
    allowed_fields = {
        'capacity': 'capacity',
        'name': 'name',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'country': 'country',
        'continent': 'continent',
        'city': 'city',
        'locationAccuracy': 'locationAccuracy',
        'capacityRating': 'capacityRating',
        'technologyType': 'technologyType',
        'status': 'status',
        'startYear': 'startYear',
        'operator': 'operator',
        'owner': 'owner',
        'wikiUrl': 'wikiUrl',
        'researchDate': 'researchDate'
    }
    # Construir colunas e valores para o update só com os campos presentes no JSON
    columns = []
    values = {}
    for key, col_name in allowed_fields.items():
        if key in data and data[key] is not None:
            columns.append(f"{col_name} = :{col_name}")
            values[col_name] = data[key]

    if not columns: return Error(code=400, message="No valid fields provided for update"), 400
    sql = f"UPDATE {stationsTable} SET {', '.join(columns)} WHERE id = :id"
    values['id'] = station_id
    try:
        db = SessionLocalStationsDB()
        db.execute(sql, values)
        db.commit()
        db.close()
        return Station.from_dict(connexion.request.get_json()), 200

    except OperationalError:
        return Error(code=503, message="Database not available"), 503

def update_station_by_id(body, station_id):  # noqa: E501
    # Update Station by Id
    if not connexion.request.is_json: return Error(code=400, message="Request body must be JSON"), 400

    data = connexion.request.get_json()

    # Prepara o SQL para substituir todos os campos
    sql = """
    UPDATE users
    SET name = :name,
        capacity = :capacity,
        latitude = :latitude,
        longitude = :longitude,
    WHERE id = :id
    """

    values = {
        'name': data['name'],
        'capacity': data['capacity'],
        'latitude': data['latitude'],
        'longitude': data['longitude'],
        'id': station_id
    }

    try:
        db = SessionLocalStationsDB()
        result = db.execute(sql, values)
        db.commit()
        db.close()

        # Se não existia utilizador com esse id, pode ser bom verificar se houve update
        if result.rowcount == 0:
            return Error(code=404, message="Station not found"), 404

        # Retorna o user atualizado
        return Station.from_dict(data), 200

    except OperationalError:
        return Error(code=503, message="Database not available"), 503

def delete_station_by_id(station_id):  # noqa: E501
    # Delete Station by Id
    try:
        db = SessionLocalStationsDB()
        sql = f"DELETE FROM {stationsTable} WHERE id = :id"
        result = db.execute(sql, {"id": station_id})
        db.commit()
        db.close()

        if result.rowcount == 0:
            return Error(code=404, message="Station not found"), 404

        return '', 204
    except OperationalError:
        return Error(code=503, message="Database not available"), 503