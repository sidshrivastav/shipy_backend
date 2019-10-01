from math import floor
from random import random
import pyqrcode, os, sys
import googlemaps
from datetime import datetime

from api import db
from api.models import order as OrderModel

gmaps = googlemaps.Client(key=os.getenv('GMAP_API'))


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
    if updates['current_status'] == 'CancelledOrder':
        similar_order = OrderModel.Order.query \
            .with_entities(OrderModel.Order.order_id, OrderModel.Order.delivery_latitude, OrderModel.Order.delivery_longitude)\
            .filter(OrderModel.Order.product_id == this_order.product_id,
                    OrderModel.Order.current_status == 'NewOrder',
                    OrderModel.Order.order_id != this_order.order_id)\
            .all()
        origin = "28.704060,77.102493"
        similar_order_data = []
        min_distance = sys.maxsize
        min_duration = sys.maxsize
        redirection_order = -1
        for order in similar_order:
            destination = str(order[1])+','+str(order[2])
            now = datetime.now()
            directions_result = gmaps.directions(origin,
                                                 destination,
                                                 mode="transit",
                                                 departure_time=now)
            if directions_result[0]['legs'][0]['distance']['value'] < min_distance\
                and directions_result[0]['legs'][0]['duration']['value'] < min_duration:
                min_distance = directions_result[0]['legs'][0]['distance']['value']
                min_duration = directions_result[0]['legs'][0]['duration']['value']
                redirection_order = order[0]
        destination = str(this_order.delivery_start_latitude) + ',' + str(this_order.delivery_start_longitude)
        directions_result = gmaps.directions(origin,
                                             destination,
                                             mode="transit",
                                             departure_time=now)
        if directions_result[0]['legs'][0]['distance']['value'] < min_distance \
                and directions_result[0]['legs'][0]['duration']['value'] < min_duration:
            this_order.current_status = 'OrdersReturned'
        else:
            this_order.current_status = 'RedirectedOrders'
            redirected_order = OrderModel.Order.query.filter_by(
                order_id=redirection_order).first()
            this_order.delivery_address = redirected_order.delivery_address
            redirected_order.current_status = 'DeliveryOnProgress'
    db.session.commit()
    return {'message': 'updated!'}, 200


def generate_special_code():
    digits = "0123456789"
    code = ""
    for iterator in range(8):
        code += digits[floor(random() * 10)]
    return code


def generate_qr(id):
    url = pyqrcode.create(os.getenv('BASE_URL')+'/api/address?order_id=' + str(id))
    url.svg('order_'+str(id)+'.svg', scale=8)
    return('order_' + str(id) + '.svg')