from swagger_server.models.response_station import ResponseStation
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

        sql = f"INSERT INTO {stationsTable} ({', '.join(columns)}) VALUES ({', '.join(placeholders)}) RETURNING *"

        try:
            db = SessionLocalStationsDB()
            row = db.execute(sql, values).fetchone()
            db.commit()
            db.close()
            return ResponseStation.from_dict(dict(row._mapping)), 201

        except OperationalError:
            return Error(code=503, message="Database not available"), 503

    return Error(code=400, message="Invalid input"), 400

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
    
def get_station_by_id(station_id):  # noqa: E501
    """Get Station by Id"""
    try:
        db = SessionLocalStationsDB()
        sql = f"SELECT * FROM {stationsTable} WHERE id = :id"
        result = db.execute(sql, {"id": station_id}) 
        row = result.fetchone()
        db.close()

        if row is None: return Error(code=404, message="Station not found"), 404

        station = ResponseStation(**row._asdict())
        return station, 200

    except OperationalError as e:
        return Error(code=503, message="Database not available"), 503
    
def get_all_stations(offset=0, limit=0, search=""):
    try:
        db = SessionLocalStationsDB()
        search_term = f"%{search.lower()}%"

        if search:
            base_query = f"""
                SELECT * FROM {stationsTable}
                WHERE LOWER(name) LIKE :search
                   OR LOWER(status) LIKE :search
                   OR LOWER(country) LIKE :search
                   OR LOWER(owner) LIKE :search
            """

            
        else:
            base_query = f"SELECT * FROM {stationsTable}"

        base_query += " ORDER BY capacity DESC"

        if limit > 0:
            base_query += " LIMIT :limit OFFSET :offset"
            params = {"search": search_term, "limit": limit, "offset": offset} if search else {"limit": limit, "offset": offset}
        else:
            base_query += " OFFSET :offset"
            params = {"search": search_term, "offset": offset} if search else {"offset": offset}

        result = db.execute(base_query, params)
        rows = result.fetchall()
        db.close()

        stations = [ResponseStation(**row._asdict()) for row in rows]
        return stations, 200

    except OperationalError:
        return Error(code=503, message="Database not available"), 500
    except Exception as e:
        return Error(code=500, message=f"Unexpected error: {e}"), 500
    
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
    sql = f"UPDATE {stationsTable} SET {', '.join(columns)} WHERE id = :id RETURNING *"
    values['id'] = station_id
    try:
        db = SessionLocalStationsDB()
        row = db.execute(sql, values).fetchone()
        db.commit()
        db.close()
        return ResponseStation.from_dict(dict(row._mapping)), 201
    
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
    RETURNING *
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
        row = db.execute(sql, values).fetchone()
        db.commit()
        db.close()
            
        if row.rowcount == 0:
            return Error(code=404, message="Station not found"), 404

        return ResponseStation.from_dict(dict(row._mapping)), 201

    except OperationalError:
        return Error(code=503, message="Database not available"), 503
