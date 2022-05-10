from flask import Flask
from flask_restful import Api

from src.resources import Project

import logging

def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Project, '/api/v1/projects')

    app.run(debug=False, port = 11415, host = '0.0.0.0')

if __name__ == '__main__':
    main()