from flask.ext.restful import Resource, abort

from models import Project, ProjectProgress

class ProjectResource(Resource):
    def get(self, project_id=None):
        project_query = Project.query

        if project_id:
            project_query = project_query.filter(Project.id == project_id)

        return [p.to_dict() for p in project_query.all()]

    def post(self):
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
            unit=request.json.get('unit')).save().to_dict()], 201  # Created

    def put(self, project_id=None):
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

        return [project.save().to_dict()]

    def delete(self, project_id=None):
        if project_id is None:
            abort(400, error='No project id specified')

        project = Project.query.get(project_id)
        if project is None:
            abort(404, error="No project with id {}".format(project_id))

        project.delete()

        return '', 204  # No content
