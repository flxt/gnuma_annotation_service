from flask import request
from flask_restful import Resource, abort

import uuid
import logging
import json


class ProjectList(Resource):

    # Get a list of all existing projects.
    def get(self):
        with open('projects.json', 'r') as file:
            projects = json.load(file)

        return list(projects.values())
    
    # Create a new project.
    def post(self):
        data = request.json

        new_id = str(uuid.uuid4())
        data['id'] = new_id

        with open('projects.json', 'r') as file:
            projects = json.load(file)

        projects[new_id] = data

        with open('projects.json', 'w') as file:
            json.dump(projects, file)

        with open('documents.json', 'r') as file:
            documents = json.load(file)

        documents[new_id] = {}

        with open('documents.json', 'w') as file:
            json.dump(documents, file)

        return new_id


class Project(Resource):

    # Delete a project.
    def delete(self, project_id):
        with open('projects.json', 'r') as file:
            projects = json.load(file)

        projects.pop(project_id, None)

        with open('projects.json', 'w') as file:
            json.dump(projects, file)

        return 200

    # Edit a project.
    def patch(self, project_id):
        with open('projects.json', 'r') as file:
            projects = json.load(file)

        for key, value in request.json.items():
            projects[project_id][key] = value

        with open('projects.json', 'w') as file:
            json.dump(projects, file)

        return 200

    # Get project metadata.
    def get(self, project_id):
        with open('projects.json', 'r') as file:
            projects = json.load(file)

        return projects[project_id]


class DocumentList(Resource):

    # Get a list of all documents in the project.
    def get(self, project_id):
        with open('documents.json', 'r') as file:
            documents = json.load(file)

        return list(documents[project_id].values())

    # Add documents to the project
    def post(self, project_id):
        data = request.json

        with open('documents.json', 'r') as file:
            documents = json.load(file)

        out = {}
        for dat in data:
            halp = {}
            halp['id'] = dat
            halp['labeled'] = False
            out[dat] = halp

        documents[project_id] = out


        with open('documents.json', 'w') as file:
            json.dump(documents, file)

        return 200


class Document(Resource):

    # Get document metadata.
    def get(self, project_id, doc_id):
        return 400

class LabelSetList(Resource):

    # Get a list of all posible label sets.
    def get(self):
        with open('labels.json', 'r') as file:
            labels = json.load(file)

        return list(labels.values())

    # Create a new label set
    def post(self):
        data = request.json

        new_id = str(uuid.uuid4())
        data['id'] = new_id

        with open('labels.json', 'r') as file:
            labels = json.load(file)

        labels[new_id] = data

        with open('labels.json', 'w') as file:
            json.dump(labels, file)

        return new_id

class LabelSet(Resource):

    def get (self, label_id):
        with open('labels.json', 'r') as file:
            labels = json.load(file)

        return labels[label_id]