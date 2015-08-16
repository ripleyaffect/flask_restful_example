from flask import request
from flask_restful import Resource, abort, marshal, marshal_with
from flask_restful_swagger import swagger

from models import Project, ProjectProgress


class ProjectListResource(Resource):
    @swagger.operation(
        notes='GET method for the ProjectList resource',
        nickname='get_project_list',
        responseMessages=[
            {
              'code': 200,
              'message': 'OK. The projects were successfully returned'
            }
          ]
        )
    @marshal_with(Project.API_REPRESENTATION, envelope='projects')
    def get(self, **kwargs):
        return Project.query.all()

    @swagger.operation(
        notes='POST method for the ProjectList resource',
        nickname='post_project_list',
        parameters=[
            {
                'allowMultiple': False,
                'dataType': 'Project',
                'description': 'A Project representation',
                'name': 'body',
                'paramType': 'body',
                'required': True
            }
        ],
        responseMessages=[
            {
              'code': 200,
              'message': 'OK. The projects were successfully created'
            },
            {
              'code': 400,
              'message': (
                'Bad request. Some fields were missing from the request')
            }
          ]
        )
    def post(self, **kwargs):
        if request.json is None:
            abort(400, error='No data provided')

        missing_fields = list(
             set(Project.REQUIRED_POST_FIELDS) - set(request.json.keys()))
        if missing_fields:
            abort(
                400,
                error='Missing field{}: {}'.format(
                    's' if len(missing_fields) > 1 else '', missing_fields))

        return marshal(
            [Project(
                title=request.json.get('title'),
                description=request.json.get('description'),
                goal=request.json.get('goal'),
                unit=request.json.get('unit')).save()],
            Project.API_REPRESENTATION, envelope='projects'), 201  # Created


class ProjectResource(Resource):
    @swagger.operation(
        notes='GET method for the Project resource',
        nickname='get_project',
        parameters=[
            {
              'name': 'project_id',
              'description': 'Id of the project to return',
              'required': True,
              'allowMultiple': False,
              'dataType': 'integer',
              'paramType': 'path'
            }
          ],
        responseMessages=[
            {
              'code': 200,
              'message': 'OK. The project was successfully returned'
            },
            {
              'code': 404,
              'message': (
                'Not found. The project with the requested Id was not found')
            }
          ]
        )
    @marshal_with(Project.API_REPRESENTATION, envelope='project')
    def get(self, project_id=None, **kwargs):
        project_query = Project.query.filter(Project.id == project_id)

        if project_query.count() == 0:
            abort(404, error='no project with id {}'.format(project_id))

        return project_query.one()

    @swagger.operation(
        notes='PUT method for the Project resource',
        nickname='put_project',
        parameters=[
            {
              'name': 'project_id',
              'description': 'Id of the project to replace',
              'required': True,
              'allowMultiple': False,
              'dataType': 'integer',
              'paramType': 'path'
            },
            {
                'allowMultiple': False,
                'dataType': 'Project',
                'description': 'A Project representation',
                'name': 'body',
                'paramType': 'body',
                'required': True
            }
          ],
          responseMessages=[
            {
              'code': 200,
              'message': 'OK. The project was successfully returned'
            },
            {
              'code': 400,
              'message': (
                'Bad request. Some fields were missing from the request')
            },
            {
              'code': 404,
              'message': (
                'Not found. The project with the requested Id was not found')
            }
          ]
        )
    @marshal_with(Project.API_REPRESENTATION, envelope='project')
    def put(self, project_id=None, **kwargs):
        missing_fields = list(
             set(Project.REQUIRED_PUT_FIELDS) - set(request.json.keys()))
        if missing_fields:
            abort(
                400,
                error='Missing field{}: {}'.format(
                    's' if len(missing_fields) > 1 else '', missing_fields))

        project = Project.query.get(project_id)
        if project is None:
            abort(404, error='No project with id {}'.format(project_id))

        project.title = request.json.get('title')
        project.description = request.json.get('description')
        project.goal = request.json.get('goal')
        project.unit = request.json.get('unit')

        return project.save()

    @swagger.operation(
        notes='DELETE method for the Project resource',
        nickname='delete_project',
        parameters=[
            {
              'name': 'project_id',
              'description': 'Id of the project to delete',
              'required': True,
              'allowMultiple': False,
              'dataType': 'integer',
              'paramType': 'path'
            }
          ],
          responseMessages=[
            {
              'code': 200,
              'message': 'OK. The project was successfully returned'
            },
            {
              'code': 404,
              'message': (
                'Not found. The project with the requested Id was not found')
            }
          ]
        )
    def delete(self, project_id=None, **kwargs):
        project = Project.query.get(project_id)
        if project is None:
            abort(404, error='No project with id {}'.format(project_id))

        project.delete()

        return '', 204  # No content
