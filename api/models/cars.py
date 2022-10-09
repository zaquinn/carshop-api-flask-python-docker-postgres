from ..utils.db import db
from enum import Enum


class Colors(Enum):
    YELLOW='Yellow'
    BLUE='Blue'
    GRAY='Gray'
    NOT_SPECIFIED = 'Not Specified'

class CarModels(Enum):
    HATCH='Hatch'
    SEDAN='Sedan'
    CONVERTIBLE='Convertible'
    NOT_SPECIFIED = 'Not Specified'

class Car(db.Model):
    __tablename__= 'cars'

    id=db.Column(db.Integer(),primary_key=True)
    model = db.Column(db.String(50),nullable=False)
    brand = db.Column(db.String(50),nullable=False)
    color = db.Column(db.Enum(Colors),default=Colors.NOT_SPECIFIED)
    car_type = db.Column(db.Enum(CarModels),default=CarModels.NOT_SPECIFIED)
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