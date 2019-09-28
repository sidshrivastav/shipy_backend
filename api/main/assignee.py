from . import api

from flask import request
from flask_restplus import Resource, fields, reqparse
from marshmallow import ValidationError

from api.models import assignee as AssigneeModel
from api.utils import assignee as AssigneeUtils

add_delivery_man_model = api.model('AddDeliveryManPayload', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email_id': fields.String(),
    'phone_no': fields.Integer(),
    'password': fields.String(),
    'current_latitude': fields.Float(),
    'current_longitude': fields.Float()
})

get_delivery_man_parser = reqparse.RequestParser()
get_delivery_man_parser.add_argument('current_latitude')
get_delivery_man_parser.add_argument('current_longitude')


@api.route('/assignee')
class Assignee(Resource):
    @api.doc(parser=get_delivery_man_parser)
    def get(self):
        pass
        # params = request.args.to_dict()
        # filters = (OrderModel.OrderSchema().load(params))
        # return OrderUtils.get_orders(filter=filters)

    @api.expect(add_delivery_man_model)
    def post(self):
        pass
        params = request.json
        if not params:
            return {'message': 'No input data provided'}, 400
        try:
            this_assignee = (AssigneeModel.AssigneeSchema().load(params))
        except ValidationError as err:
            # TODO parse the err in our format
            return {'error': err.messages, 'message': 'Input not in expected format'}, 422
        return AssigneeUtils.add_assignee(assignee=this_assignee)

    def put(self):
        pass

    def delete(self):
        pass