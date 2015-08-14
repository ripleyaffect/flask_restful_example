import uuid

from flask import request, g
from flask.ext.restful import Resource, abort, marshal
from flask_restful_swagger import swagger

from models import ProjectProgress
from logger import logger

def colorify(text, color=''):
    colors = {
        'HEADER': '\033[95m',
        'OKBLUE': '\033[94m',
        'OKGREEN': '\033[92m',
        'WARNING': '\033[93m',
        'FAIL': '\033[91m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m'}
    color = color.upper()
    if color not in colors:
        return text
    return '{}{}\033[0m'.format(colors[color], text)


def logging_dec(func):
    def inner(*args, **kwargs):
        logger.info(colorify('Here comes the request!', 'OKBLUE'))
        val = func(*args, **kwargs)
        logger.info(colorify('There goes the request!', 'OKBLUE'))
        return val
    return inner

def request_id_dec(func):
    def inner(*args, **kwargs):
        g.request_id = uuid.uuid4()
        logger.info(colorify('Request given id: {}'.format(g.request_id), 'OKGREEN'))
        val = func(*args, **kwargs)
        logger.info(colorify('Request with Id {} completed'.format(g.request_id), 'OKGREEN'))
        return val
    return inner

class ProjectProgressListResource(Resource):
    decorators = [request_id_dec, logging_dec]

    def post(self, project_id):
        if request.json is None:
            abort(400, error='No data provided')

        missing_fields = list(
             set(ProjectProgress.REQUIRED_POST_FIELDS) -
             set(request.json.keys()))
        if missing_fields:
            abort(
                400,
                error='Missing field{}: {}'.format(
                    's' if len(missing_fields) > 1 else '', missing_fields))

        return marshal(
            [ProjectProgress(
                project_id=project_id,
                value=request.json.get('value'),
                note=request.json.get('note')).save()],
            ProjectProgress.API_REPRESENTATION), 201  # Created


class ProjectProgressResource(Resource):
    decorators = [request_id_dec, logging_dec]

    def delete(self, project_id, project_progress_id):
        project_progress = ProjectProgress.query.get(project_progress_id)
        if project_progress is None:
            abort(
                404,
                error="No project progress with id {}".format(project_progress_id))
        if project_progress.project_id != project_id:
            abort(
                400,
                error=(
                    'project progress with id {} does not belong to project '
                    'with id {}'.format(project_progress_id, project_id)))

        project_progress.delete()

        return '', 204  # No content
