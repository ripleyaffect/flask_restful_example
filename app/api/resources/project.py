from flask import request
from flask_restful import Resource, abort, marshal_with, marshal, fields

from models import Project, ProjectProgress

class ProjectResource(Resource):

    @marshal_with(Project.API_REPRESENTATION)
    def get(self, project_id=None, **kwargs):
        project_query = Project.query

        if project_id:
            project_query = project_query.filter(Project.id == project_id)

        return project_query.all()

    @marshal_with(Project.API_REPRESENTATION)
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

        return [Project(
            title=request.json.get('title'),
            description=request.json.get('description'),
            goal=request.json.get('goal'),
            unit=request.json.get('unit')).save()]

    @marshal_with(Project.API_REPRESENTATION)
    def put(self, project_id=None, **kwargs):
        if project_id is None:
            abort(400, error='No project id specified')

        missing_fields = list(
             set(Project.REQUIRED_PUT_FIELDS) - set(request.json.keys()))
        if missing_fields:
            abort(
                400,
                error='Missing field{}: {}'.format(
                    's' if len(missing_fields) > 1 else '', missing_fields))

        project = Project.query.get(project_id)
        if project is None:
            abort(404, error="No project with id {}".format(project_id))

        project.title = request.json.get('title')
        project.description = request.json.get('description')
        project.goal = request.json.get('goal')
        project.unit = request.json.get('unit')

        return [project.save()]

    def delete(self, project_id=None, **kwargs):
        if project_id is None:
            abort(400, error='No project id specified')

        project = Project.query.get(project_id)
        if project is None:
            abort(404, error="No project with id {}".format(project_id))

        project.delete()

        return ''
