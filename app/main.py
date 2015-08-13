from flask import Flask, render_template
from flask.ext.restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy



# Initialize the app and configure
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


# Initialize database and ORM
db = SQLAlchemy(app)


# Initialize API and Add resoruces/routing
api = Api(app)


# Serve up the client
@app.route("/")
def index(path=None):
    return render_template('index.html')


# Run the application
if __name__ == '__main__':
    from api import ProjectResource, ProjectProgressResource
    api.add_resource(
        ProjectResource, '/api/projects', '/api/projects/<int:project_id>')
    api.add_resource(
        ProjectProgressResource,
        '/api/projects/<int:project_id>/progress',
        '/api/projects/<int:project_id>/progress/<int:project_progress_id>')
    app.run(debug=True)
