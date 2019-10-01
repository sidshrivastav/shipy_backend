from api import db, ma

from datetime import datetime


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer)
    product_title = db.Column(db.VARCHAR(10))
    product_thumbnail_url = db.Column(db.String)
    current_status = db.Column(db.VARCHAR(100), default='NewOrder')
    receiver_name = db.Column(db.String)
    delivery_start_address = db.Column(db.VARCHAR(200))
    delivery_start_latitude = db.Column(db.Float)
    delivery_start_longitude = db.Column(db.Float)
    delivery_address = db.Column(db.VARCHAR(200))
    delivery_latitude = db.Column(db.Float)
    delivery_longitude = db.Column(db.Float)
    assigned_to = db.Column(db.Integer)
    special_code = db.Column(db.VARCHAR(8))
    qr = db.Column(db.VARCHAR(1000))
    is_active = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def update_time(mapper, connection, instance):
        now = datetime.utcnow()
        instance.last_updated = now

    @classmethod
    def register(cls):
        db.event.listen(cls, 'before_update', cls.update_time)

    def __repr__(self):
        return "<Order '{}'>".format(self.order_id)


class OrderSchema(ma.ModelSchema):
    class Meta:
        model = Order

    def __repr__(self):
        return "<OrderSchema '{}'>".format(self.order_id)
