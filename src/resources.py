from flask import request
from flask_restful import Resource, abort

import uuid
import logging


class ProjectList(Resource):

    # Init the resource.
    def __init__(self, projects, documents):
        self._projects = projects
        self._documents = documents

    # Get a list of all existing projects.
    def get(self):
        logging.debug('Returning list of projects')

        out = []
        for i in self._projects.values():
            out.append(i)

        return out
    
    # Create a new project.
    def post(self):
        if not request.is_json:
            abort(400, 'No JSON Sadge.')

        new_id = str(uuid.uuid4())

        data = request.json
        data['id'] = new_id

        self._projects[new_id] = data
        self._documents[new_id] = {}

        logging.debug(f'Added Project with id {new_id}')

        return new_id


class Project(Resource):

    # Init the resource.
    def __init__(self, projects):
        self._projects = projects

    # Delete a project.
    def delete(self, project_id):
        logging.debug(f'Deleting project {project_id}')

        self._projects.pop(project_id, None)

        return 200

    # Edit a project.
    def patch(self, project_id):
        if not request.is_json:
            abort(400, 'No JSON Sadge.')

        logging.debug(request.json)

        for key, value in request.json.items():
            self._projects[project_id][key] = value

        logging.debug(f'Patching project {project_id}')

        return 200

    # Get project metadata.
    def get(self, project_id):
        logging.debug(f'Getting meta data for project {project_id}')

        return self._projects[project_id]


class DocumentList(Resource):

    # Init the resource.
    def __init__(self, documents):
        self._documents = documents

    # Get a list of all documents in the project.
    def get(self, project_id):
        logging.debug('Returning list of documents')

        out = []
        for i in self._documents[project_id].values():
            out.append(i)

        return out

    # Upload a document to the project
    def post(self, project_id):
        if not request.is_json:
            abort(400, 'No JSON Sadge.')

        new_id = str(uuid.uuid4())

        data = request.json
        data['id'] = new_id

        self._documents[project_id][new_id] = data

        logging.debug(f'Uploading document {new_id} to project {project_id}')

        return new_id


class Document(Resource):

    # Init the resource.
    def __init__(self, documents):
        self._documents = documents

    # Delete a document.
    def delete(self, project_id, doc_id):
        logging.debug(f'Deleting document {doc_id}')

        self._documents[project_id].pop(doc_id, None)

        return 200

    # Edit a document.
    def patch(self, project_id, doc_id):
        if not request.is_json:
            abort(400, 'No JSON Sadge.')

        for key, value in request.json.items():
            self._documents[project_id][doc_id][key] = value

        logging.debug(f'Patching document {doc_id}')

        return 200

    # Get document metadata.
    def get(self, project_id, doc_id):
        logging.debug(f'Getting meta data for document {doc_id}')

        return self._documents[project_id][doc_id]