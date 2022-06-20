from flask import request
from flask_restful import Resource, abort

import pymongo
import uuid
import json

from src.util import logwrapper

# Get a list of projects or create a new project.
class ProjectList(Resource):

    # Init the resource.
    def __init__(self, anno_db):
        self._project_col = anno_db['projects'] 

    # Get a list of all existing projects.
    def get(self):
        projects = self._project_col.find({'alive': True}, {'alive': 0})
        projects = list(projects)

        logwrapper.debug(f'Projects: {projects}')

        return projects
    
    # Create a new project.
    def post(self):
        data = request.json

        new_id = str(uuid.uuid4())
        data['_id'] = new_id
        data['id'] = new_id
        data['alive'] = True

        self._project_col.insert_one(data)

        logwrapper.info(f'Inserted new project with id {new_id}.')

        return new_id

# Handle one specific project.
class Project(Resource):

    # Init the resource.
    def __init__(self, anno_db):
        self._project_col = anno_db['projects'] 

    # Delete a project.
    def delete(self, project_id):
        self._project_col.update_one({'_id': project_id}, {'$set': {'alive': False}})

        return 200

    # Edit a project.
    def patch(self, project_id):
        for key, value in request.json.items():
            self._project_col.update_one({'_id': project_id}, {'$set': {key: value}})

        return 200

    # Get project metadata.
    def get(self, project_id):
        project = self._project_col.find_one({'_id': project_id}, {'alive': 0})

        logwrapper.debug(f'id: {project_id} - project: {project}')

        if (not project):
            abort(400, messsage=f'No label set with id {project_id} exists.')

        return project


# Get a list of documents in a project.
class DocumentList(Resource):

    # Get a list of all documents in the project.
    def get(self, project_id):
        return [
            {'id': 1, 'labeled': False},
            {'id': 2, 'labeled': True},
            {'id': 3, 'labeled': False},
        ]

    # Add documents to the project
    def post(self, project_id):
        return 200


# Handle one document
class Document(Resource):

    # Get document labels and relations.
    def get(self, project_id, doc_id):
        return {
            'labels': [],
            'relations': []
        }

    # Remove a document from the project
    def delete(self, project_id, doc_id):
        return 200

# Get a list of label sets or create a new one.
class LabelSetList(Resource):

    # Init the resource.
    def __init__(self, anno_db):
        self._label_set_col = anno_db['label_sets'] 

    # Get a list of all posible label sets.
    def get(self):
        label_sets = self._label_set_col.find()
        label_sets = list(label_sets)

        logwrapper.debug(f'Label sets: {label_sets}')

        return label_sets

    # Create a new label set
    def post(self):
        data = request.json

        new_id = str(uuid.uuid4())
        data['_id'] = new_id
        data['id'] = new_id

        self._label_set_col.insert_one(data)

        logwrapper.info(f'Inserted new label set with id {new_id}.')

        return new_id

# Get info for one label set.
class LabelSet(Resource):

    # Init the resource.
    def __init__(self, anno_db):
        self._label_set_col = anno_db['label_sets'] 

    def get (self, label_id):
        label_set = self._label_set_col.find_one({'_id': label_id})

        logwrapper.debug(f'id: {label_id} - label set: {label_set}')

        if (not label_set):
            abort(400, messsage=f'No label set with id {label_id} exists.')

        return label_set