from ..utils.db import db
from enum import Enum


class Car(db.Model):
    __tablename__= 'cars'

    id=db.Column(db.Integer(),primary_key=True)
    model = db.Column(db.String(50),nullable=False)
    brand = db.Column(db.String(50),nullable=False)
    color = db.Column(db.Enum("Yellow", "Blue", "Gray", "Not Specified", name="color_choices"), server_default="Not Specified")
    car_type = db.Column(db.Enum("Sedan","Hatch","Convertible","Not Specified", name="cartype_choices"), server_default="Not Specified")
    owner=db.Column(db.Integer(),db.ForeignKey('citizens.id'))
    

    def __repr__(self):
        f"<Car {self.id} {self.name}>"


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()