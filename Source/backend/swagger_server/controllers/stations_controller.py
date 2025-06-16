import connexion
from sqlalchemy.exc import OperationalError
from swagger_server.db.session import SessionLocalStationsDB
from swagger_server.models.error import Error  # modelo gerado
from swagger_server.models.station import Station  # modelo gerado (Swagger)
from swagger_server.db.session import stationsTable
def station_post(body):  # noqa: E501
    """Creates a station."""
    if connexion.request.is_json:
        # Campos que vamos aceitar, obrigatórios + opcionais do schema
    
        allowed_fields = {
            'capacity': 'capacity_mw',
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

def station_station_id_get(station_id):  # noqa: E501
    """Get Station by Id"""
    try:
        db = SessionLocalStationsDB()
        sql = f"SELECT country, continent, city FROM {stationsTable} WHERE id = :id"
        result = db.execute(sql, {"id": station_id}) 
        row = result.fetchone()
        db.close()

        if row is None: return Error(code=404, message="Station not found"), 404

        station = Station(id=row.id,country=row.country, continent=row.continent, city=row.city)
        return station, 200

    except OperationalError as e:
        return Error(code=503, message="Database not available"), 503
