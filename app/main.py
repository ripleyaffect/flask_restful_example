from flask import Flask, render_template
from flask.ext.restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful_swagger import swagger


# Initialize the app and configure
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


# Initialize database and ORM
db = SQLAlchemy(app)


# Initialize API and Add resoruces/routing
api = swagger.docs(Api(app), apiVersion='0.1')


# Serve up the client
@app.route("/")
def index(path=None):
    return render_template('index.html')


# Run the application
if __name__ == '__main__':
    from api import (
      ProjectResource, ProjectListResource,
      ProjectProgressResource, ProjectProgressListResource)
    api.add_resource(ProjectListResource, '/api/projects')
    api.add_resource(ProjectResource, '/api/projects/<int:project_id>')
    api.add_resource(
      ProjectProgressListResource, '/api/projects/<int:project_id>/progress')
    api.add_resource(
        ProjectProgressResource,
        '/api/projects/<int:project_id>/progress/<int:project_progress_id>')
    app.run(debug=True)
