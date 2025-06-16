#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_cors import CORS

import os


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'GeoSolar'}, pythonic_params=True)
    
    CORS(app.app, resources={r"/*": {"origins":"*"}}, allow_headers="*", methods=["GET","POST","PUT","DELETE","OPTIONS"])
    app.run(host="0.0.0.0", port=int(os.getenv("MYPORT")))

if __name__ == '__main__':
    main()
