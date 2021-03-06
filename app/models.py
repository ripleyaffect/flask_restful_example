from __future__ import absolute_import

import datetime

from flask.ext.restful import fields

from main import db
from logger import logger


class ModelUtils(object):
    """Mixin to provide convenience operations to SQLAlchemy Models"""
    def save(self, commit=True):
        """Add `self` to the current session and optionally commits

        :param commit: `bool` flag to optionally commit the change
            default: True
        :returns: `self` if successful, otherwise raises error

        """
        db.session.add(self)
        if commit:
            db.session.commit()
            logger.info(
                '{} {} saved'.format(self.__class__.__name__, self.id))
        return self

    def delete(self, commit=True):
        """Removes `self` to the current session and optionally commits

        :param commit: `bool` flag to optionally commit the change
            default: True
        :returns: `True` if successful, otherwise raises an error

        """
        db.session.delete(self)
        if commit:
            db.session.commit()
            logger.info(
                '{} {} deleted'.format(self.__class__.__name__, self.id))
        return True


class ProjectProgress(db.Model, ModelUtils):
    __tablename__ = 'project_progress'

    id = db.Column(db.Integer, primary_key=True)
    created_asof = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_asof = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship(
        'Project', backref="progress", foreign_keys=[project_id])

    value = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    REQUIRED_POST_FIELDS = ['value']

    API_REPRESENTATION = {
        'id': fields.Integer,
        'created_asof': fields.DateTime,
        'updated_asof': fields.DateTime,

        'project_id': fields.Integer,
        'value': fields.Integer,
        'notes': fields.String
    }


class Project(db.Model, ModelUtils):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    created_asof = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_asof = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    goal = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Text, nullable=False, default="hours")

    REQUIRED_POST_FIELDS = ['title', 'description', 'goal', 'unit']
    REQUIRED_PUT_FIELDS = ['title', 'description', 'goal', 'unit']

    API_REPRESENTATION = {
        'id': fields.Integer,
        'created_asof': fields.DateTime,
        'updated_asof': fields.DateTime,

        'title': fields.String,
        'description': fields.String,
        'goal': fields.Integer,
        'unit': fields.String,
        'progress': fields.Nested(ProjectProgress.API_REPRESENTATION)
    }
