FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

# Atualiza a variável de ambiente para correr o Flask na porta 80 e em todas as interfaces
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80
ENV PYTHONUNBUFFERED=1

CMD ["flask", "run"]
