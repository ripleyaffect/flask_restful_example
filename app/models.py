from __future__ import absolute_import

import datetime

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

    def to_dict(self):
        """Return a dictionary representation of this instance

        `datetime` objects are turned into isoformt `str`s if present

        """
        return {
            'id': self.id,
            'created_asof': self.created_asof.isoformat(),
            'updated_asof': (
                self.updated_asof.isoformat() if self.updated_asof else None),
            'title': self.title,
            'description': self.description,
            'goal': self.goal,
            'unit': self.unit,
            'progress': [p.to_dict() for p in self.progress]}


class ProjectProgress(db.Model, ModelUtils):
    __tablename__ = 'project_progress'

    id = db.Column(db.Integer, primary_key=True)
    created_asof = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_asof = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship(
        Project, backref="progress", foreign_keys=[project_id])

    value = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    REQUIRED_POST_FIELDS = ['value']

    def to_dict(self):
        """Return a dictionary representation of this instance

        `datetime` objects are turned into isoformt `str`s if present

        """
        return {
            'id': self.id,
            'created_asof': self.created_asof.isoformat(),
            'updated_asof': (
                self.updated_asof.isoformat() if self.updated_asof else None),
            'project_id': self.project_id,
            'value': self.value,
            'note': self.note}
