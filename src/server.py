from flask import Flask
from flask_restful import Api
from flask_cors import CORS

import pymongo

from src.api.resources import Project, ProjectList, Document, DocumentList, LabelSetList, LabelSet
from src.util import logwrapper

def main():

    # Set up Flask and the Rest API.
    app = Flask(__name__)
    api = Api(app)

    # Define CORS settings.
    cors = CORS(app, resources={
        r'/api/*': {
            'origins': '*'
        }
    })

    # Connect to MongoDB
    mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
    anno_db = mongo_client['anno_db']

    # Add resources to the API.
    pre = '/api/v1'
    api.add_resource(ProjectList, f'{pre}/projects', resource_class_kwargs={'anno_db': anno_db})
    api.add_resource(Project, f'{pre}/projects/<project_id>', resource_class_kwargs={'anno_db': anno_db})
    api.add_resource(DocumentList, f'{pre}/projects/<project_id>/docs')
    api.add_resource(Document, f'{pre}/projects/<project_id>/docs/<doc_id>')
    api.add_resource(LabelSetList, f'{pre}/labels', resource_class_kwargs={'anno_db': anno_db})
    api.add_resource(LabelSet, f'{pre}/labels/<label_id>', resource_class_kwargs={'anno_db': anno_db})

    # Start the server.
    app.run(debug=False, port = 11415, host = '0.0.0.0')

if __name__ == '__main__':
    main()