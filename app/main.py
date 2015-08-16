from flask import Flask, render_template
from flask.ext.restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful_swagger import swagger


# Initialize the app and configure
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['PROPAGATE_EXCEPTIONS'] = False


# Initialize database and ORM
db = SQLAlchemy(app)



def initialize_api(app):
    """Initialize API and Add resoruces/routing
    """
    from resources import (
        ProjectResource, ProjectListResource,
        ProjectProgressResource, ProjectProgressListResource)

    errors = {
      'NegativeProgressError': {
          'message': 'Progress can only be positive.',
          'status': 400,
      }
    }

    api = swagger.docs(Api(app, errors=errors), apiVersion='0.1')

    api.add_resource(ProjectListResource, '/api/projects')
    api.add_resource(ProjectResource, '/api/projects/<int:project_id>')
    api.add_resource(
      ProjectProgressListResource, '/api/projects/<int:project_id>/progress')
    api.add_resource(
        ProjectProgressResource,
        '/api/projects/<int:project_id>/progress/<int:project_progress_id>')

    return api


# Serve up the client
@app.route("/")
def index(path=None):
    return render_template('index.html')


# Run the application
if __name__ == '__main__':
    initialize_api(app)
    app.run(debug=True)
