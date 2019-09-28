from api import db, ma

from datetime import datetime


class Assignee(db.Model):
    __tablename__ = 'assignee'

    assignee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.VARCHAR(10))
    last_name = db.Column(db.VARCHAR(10))
    email_id = db.Column(db.VARCHAR(250))
    phone_no = db.Column(db.VARCHAR(10))
    password = db.Column(db.VARCHAR(10), nullable=False)
    current_latitude = db.Column(db.Float)
    current_longitude = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def update_time(mapper, connection, instance):
        now = datetime.utcnow()
        instance.last_updated = now

    @classmethod
    def register(cls):
        db.event.listen(cls, 'before_update', cls.update_time)

    def __repr__(self):
        return "<Assignee '{}'>".format(self.assignee_id)


class AssigneeSchema(ma.ModelSchema):
    class Meta:
        model = Assignee

    def __repr__(self):
        return "<AssigneeSchema '{}'>".format(self.order_id)
