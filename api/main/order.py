from . import api

from flask import request
from flask_restplus import Resource, fields, reqparse
from marshmallow import ValidationError

from api.models import order as OrderModel
from api.utils import order as OrderUtils

add_order_model = api.model('AddOrderPayload', {
    'product_id': fields.Integer(),
    'product_title': fields.String(),
    'product_thumbnail_url': fields.String(),
    'receiver_name': fields.String(),
    'delivery_address': fields.String(),
    'delivery_latitude': fields.Float(),
    'delivery_longitude': fields.Float(),
    'assigned_to': fields.Integer()
})

get_order_parser = reqparse.RequestParser()
get_order_parser.add_argument('order_id')
get_order_parser.add_argument('assigned_to')
get_order_parser.add_argument('current_status')
# NewOrder, DeliveryOnProgress, CancelledOrder, RedirectedOrders, OrdersReturned

update_order_parser = reqparse.RequestParser()
update_order_parser.add_argument('order_id')
update_order_parser.add_argument('assigned_to')
update_order_parser.add_argument('current_status')
update_order_parser.add_argument('delivery_address')

get_address_parser = reqparse.RequestParser()
get_address_parser.add_argument('order_id')


@api.route('/order')
class Order(Resource):
    @api.doc(parser=get_order_parser)
    def get(self):
        params = request.args.to_dict()
        filters = (OrderModel.OrderSchema().load(params))
        return OrderUtils.get_orders(filter=filters)

    @api.expect(add_order_model)
    def post(self):
        params = request.json
        if not params:
            return {'message': 'No input data provided'}, 400
        try:
            this_order = (OrderModel.OrderSchema().load(params))
        except ValidationError as err:
            # TODO parse the err in our format
            return {'error': err.messages, 'message': 'Input not in expected format'}, 422
        return OrderUtils.add_order(order=this_order)

    @api.doc(parser=update_order_parser)
    def put(self):
        params = request.args.to_dict()
        updates = (OrderModel.OrderSchema().load(params))
        return OrderUtils.update_orders(update=updates)

    def delete(self):
        pass


@api.route('/address')
class Address(Resource):
    @api.doc(parser=get_address_parser)
    def get(self):
        params = request.args.to_dict()
        filters = (OrderModel.OrderSchema().load(params))
        return OrderUtils.get_address(filter=filters)
