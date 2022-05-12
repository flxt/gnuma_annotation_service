from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from src.resources import Project, ProjectList, Document, DocumentList

import logging

def main():
    # Set up logger.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    # Set up Flask and the Rest API.
    app = Flask(__name__)
    api = Api(app)

    # Define CORS settings.
    cors = CORS(app, resources={
        r'/api/*': {
            'origins': '*'
        }
    })

    # Define project storage. TODO: remove
    projects = {}
    documents = {}

    # Add resources to the API.
    pre = '/api/v1'
    api.add_resource(ProjectList, f'{pre}/projects', resource_class_kwargs={'projects': projects})
    api.add_resource(Project, f'{pre}/projects/<project_id>', resource_class_kwargs={'projects': projects})
    api.add_resource(DocumentList, f'{pre}/projects/<project_id>/docs', resource_class_kwargs={'documents': documents})
    api.add_resource(Document, f'{pre}/projects/<project_id>/docs/<doc_id>', resource_class_kwargs={'documents': documents})

    # Start the server.
    app.run(debug=False, port = 11415, host = '0.0.0.0')

if __name__ == '__main__':
    main()