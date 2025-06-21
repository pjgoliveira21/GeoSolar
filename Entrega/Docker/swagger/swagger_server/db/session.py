from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# DB1
STATIONS_DB_URL = os.getenv("STATIONS_DB_URL")
engine_stations_db = create_engine(STATIONS_DB_URL)
SessionLocalStationsDB = sessionmaker(bind=engine_stations_db)
stationsTable="solar_power_stations"

# DB2
USERS_DB_URL = os.getenv("USERS_DB_URL")
engine_users_db = create_engine(USERS_DB_URL)
SessionLocalUsersDB = sessionmaker(bind=engine_users_db)
usersTable="users"