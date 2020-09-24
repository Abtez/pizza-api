from app import db
from datetime import datetime

class Pizza(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    size = db.Column(db.String())
    price = db.Column(db.String())
    crust = db.Column(db.String())

    def __init__(self, id, name, size, price, crust):
        """initialize with name."""
        self.id =id
        self.name = name
        self.size = size
        self.price = price
        self.crust= crust        

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Pizza.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Pizza: {}>".format(self.name)