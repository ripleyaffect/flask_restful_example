import uuid

from flask import request, g
from flask.ext.restful import Resource, abort, marshal
from flask_restful_swagger import swagger

from models import Project, ProjectProgress
from logger import logger

def colorify(text, color=''):
    colors = {
        'BLUE': '\033[94m',
        'GREEN': '\033[92m',
        'RED': '\033[91m',}
    color = color.upper()
    if color not in colors:
        return text
    return '{}{}\033[0m'.format(colors[color], text)


def post_logging_dec(func):
    def inner(*args, **kwargs):
        if request.json:
            logger.info(
                colorify(
                    'Here comes a progress POST request for project '
                    '{}: {}!'.format(
                        request.view_args.get('project_id'),
                        request.json), 'BLUE'))
        else:
            logger.info(
                colorify(
                    'A progress request came in with no data!', 'RED'))

        val = func(*args, **kwargs)

        logger.info(colorify('There goes the progress request!', 'BLUE'))
        return val
    return inner


def delete_logging_dec(func):
    def inner(*args, **kwargs):
        logger.info(
            colorify(
                'Here comes a progress DELETE request '
                'for project {} and progress {}'.format(
                    request.view_args.get('project_id'),
                    request.view_args.get('project_progress_id')), 'BLUE'))

        val = func(*args, **kwargs)

        logger.info(colorify('There goes the progress request!', 'BLUE'))
        return val
    return inner


def request_id_dec(func):
    def inner(*args, **kwargs):
        g.request_id = uuid.uuid4()
        logger.info(
            colorify('Request given id: {}'.format(g.request_id), 'GREEN'))
        val = func(*args, **kwargs)
        logger.info(
            colorify(
                'Request with Id {} completed'.format(g.request_id), 'GREEN'))
        return val
    return inner


class ProgressLoggingResource(Resource):
    """Add a decorator to all subclasses of LoggingResource"""
    method_decorators = [request_id_dec]


class NegativeProgressError(Exception):
    pass


class ProjectProgressListResource(ProgressLoggingResource):
    decorators = [post_logging_dec]

    @swagger.operation(
        notes='POST method for the ProjectProgressList resource',
        nickname='post_project_progress_list',
        parameters=[
            {
                'name': 'project_id',
                'description': "Id of the project that the progress is for",
                'required': True,
                'allowMultiple': False,
                'dataType': 'integer',
                'paramType': 'path'
            },
            {
                'allowMultiple': False,
                'dataType': 'Project',
                'description': 'A ProjectProgress representation',
                'name': 'body',
                'paramType': 'body',
                'required': True
            }
        ],
        responseMessages=[
            {
                'code': 200,
                'message': 'OK. The project progress was successfully created'
            },
            {
                'code': 400,
                'message': (
                    'Bad request. Some fields were missing from the request')
            },
            {
                'code': 404,
                'message': (
                    'Not found. The project with the requested '
                    'Id was not found')
            }
          ]
        )
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

        # if int(request.json.get('value')) <= 0:
        #     raise NegativeProgressError()

        if Project.query.filter(Project.id == project_id).count() == 0:
            abort(404, error='No project with id "{}"'.format(project_id))

        return marshal(
            [ProjectProgress(
                project_id=project_id,
                value=request.json.get('value'),
                note=request.json.get('note')).save()],
            ProjectProgress.API_REPRESENTATION,
            envelope='progress'), 201  # Created


class ProjectProgressResource(ProgressLoggingResource):
    decorators = [delete_logging_dec]

    @swagger.operation(
        notes='DELETE method for the ProjectProgress resource',
        nickname='delete_project_progress',
        parameters=[
            {
                'name': 'project_id',
                'description': "Id of the project who's progress to delete",
                'required': True,
                'allowMultiple': False,
                'dataType': 'integer',
                'paramType': 'path'
            },
            {
                'name': 'project_progress_id',
                'description': 'Id of the project progress to delete',
                'required': True,
                'allowMultiple': False,
                'dataType': 'integer',
                'paramType': 'path'
            }
          ],
          responseMessages=[
            {
              'code': 204,
              'message': 'No content. The progress was successfully deleted'
            },
            {
              'code': 400,
              'message': (
                'Bad request. The progress with the requested Id does not '
                'belong to the requestsed project')
            },
            {
              'code': 404,
              'message': (
                'Not found. The progress with the requested Id was not found')
            }
          ]
        )
    def delete(self, project_id, project_progress_id):
        project_progress = ProjectProgress.query.get(project_progress_id)
        if project_progress is None:
            abort(
                404,
                error=(
                    "No project progress with id {}".format(
                        project_progress_id)))
        if project_progress.project_id != project_id:
            abort(
                400,
                error=(
                    'project progress with id {} does not belong to project '
                    'with id {}'.format(project_progress_id, project_id)))

        project_progress.delete()

        return '', 204  # No content
