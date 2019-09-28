from math import floor
from random import random
import pyqrcode

from api import db
from api.models import order as OrderModel


def add_order(**kwargs):
    kwargs['order'].special_code = generate_special_code()
    db.session.add(kwargs['order'])
    db.session.flush()
    kwargs['order'].qr = generate_qr(kwargs['order'].order_id)
    db.session.commit()
    return {'message': 'Added'}, 200


def get_orders(**kwargs):
    # NewOrder, DeliveryOnProgress, CancelledOrder, RedirectedOrders, OrdersReturned
    filters = (OrderModel.OrderSchema().dump(kwargs['filter']))
    these_order = OrderModel.Order.query
    for attr, value in filters.items():
        if value is not None:
            these_order = these_order.filter(getattr(OrderModel.Order, attr) == value)
    these_order = these_order.all()
    these_order = OrderModel.OrderSchema().dump(these_order, many=True)
    return these_order, 200


def get_address(**kwargs):
    # NewOrder, DeliveryOnProgress, CancelledOrder, RedirectedOrders, OrdersReturned
    filters = (OrderModel.OrderSchema().dump(kwargs['filter']))
    these_order = OrderModel.Order.query
    for attr, value in filters.items():
        if value is not None:
            these_order = these_order.filter(getattr(OrderModel.Order, attr) == value)
    these_order = these_order.first()
    these_order = OrderModel.OrderSchema().dump(these_order)
    return {'name':these_order['receiver_name'],'address':these_order['delivery_address'],'special_code':these_order['special_code'],}, 200


def update_orders(**kwargs):
    this_order = OrderModel.Order.query.filter_by(
        order_id=kwargs['update'].order_id).first()
    updates = (OrderModel.OrderSchema().dump(kwargs['update']))
    for attr, value in updates.items():
        if value is not None:
            this_order.attr = value
    db.session.commit()
    return {'message': 'updated!'}, 200


def generate_special_code():
    digits = "0123456789"
    code = ""
    for iterator in range(8):
        code += digits[floor(random() * 10)]
    return code


def generate_qr(id):
    url = pyqrcode.create('http://00901c70.ngrok.io/api/address?order_id=' + str(id))
    url.svg('order_'+str(id)+'.svg', scale=8)
    return('order_' + str(id) + '.svg')

