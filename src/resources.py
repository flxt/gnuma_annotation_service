from flask import request
from flask_restful import Resource, abort

import uuid
import logging


class Project(Resource):

    def __init__(self):
        project_list = [{'id': '123', 'name': 'Test project 1'}, {'id': '3453', 'name': 'Test project 2'}]

    def get(self):
        logging.debug('Returning list of projects')

        return project_list
        
    def post(self):
        new_project = {'id': uuid.uuid4(), 'name': 'Test'}

        project_list.append(new_project)

        logging.debug(f'Added Project with id {new_project["id"]}')

        return new_project

    def delete(self):
        return {}
