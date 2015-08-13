from flask import request
from flask.ext.restful import Resource, abort

from models import ProjectProgress


class ProjectProgressResource(Resource):
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

        return [ProjectProgress(
            project_id=project_id,
            value=request.json.get('value'),
            note=request.json.get('note')).save().to_dict()], 201  # Created

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
