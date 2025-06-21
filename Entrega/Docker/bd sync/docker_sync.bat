@echo off
if /i "%~1"=="upload" (
    echo "[+] Extracting database..."
    docker exec -t Postgres-Users-Database pg_dumpall -U root > users.sql
    docker exec -t Postgres-Stations-Database pg_dumpall -U root > stations.sql
    pause
    exit /b
)

if /i "%~1"=="download" (
    echo "[+] Importing database..."
    docker cp users.sql Postgres-Users-Database:/users.sql
    docker exec -i Postgres-Users-Database psql -U root -d users -f /users.sql

    docker cp stations.sql Postgres-Stations-Database:/stations.sql
    docker exec -i Postgres-Stations-Database psql -U root -d stations -f /stations.sql
    pause
    exit /b
)

echo Erro: Argumento inválido. Use "upload" ou "download".
pause
exit /b
