from api import db

from api.models import assignee as AssigneeModel


def add_assignee(**kwargs):
    db.session.add(kwargs['assignee'])
    db.session.commit()
    return {'message': 'Added'}, 200


def get_assignee(**kwargs):
    filters = (AssigneeModel.AssigneeSchema().dump(kwargs['filter']))
    these_assignee = AssigneeModel.Assignee.query
    for attr, value in filters.items():
        try:
            these_assignee = these_assignee.filter(getattr(AssigneeModel, attr) == value)
        except AttributeError:
            pass
    these_assignee = these_assignee.all()
    these_assignee = AssigneeModel.AssigneeSchema().dump(these_assignee, many=True)
    return these_assignee, 200
