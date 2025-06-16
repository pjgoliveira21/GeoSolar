import connexion
from sqlalchemy.exc import OperationalError
from swagger_server.db.session import SessionLocalStationsDB
from swagger_server.models.error import Error  # modelo gerado
from swagger_server.models.station import Station  # modelo gerado (Swagger)
from swagger_server.db.session import stationsTable
def station_post(body):  # noqa: E501
    """Creates a station."""
    if connexion.request.is_json:
        body = Station.from_dict(connexion.request.get_json())  # objeto com name, lat, lon, etc.

        try:
            db = SessionLocalStationsDB()
            sql= f"INSERT INTO {stationsTable} (name, latitude, longitude) VALUES (:name, :lat, :lon)"
            db.execute(sql,{"name": body.name, "lat": body.lat, "lon": body.lon})
            db.commit()
            db.close()
            return body, 201

        except OperationalError as e:
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

        # Simulando um objeto Station com base em resultado SQL (ajusta conforme modelo Swagger)
        print(row)
        station = Station(country=row.country, continent=row.continent, city=row.city)
        return station, 200

    except OperationalError as e:
        return Error(code=503, message="Database not available"), 503
