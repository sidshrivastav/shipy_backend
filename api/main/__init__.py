from flask_restplus import Api, Namespace

api = Namespace('api', description='Shipy APIs')

from . import order, assignee