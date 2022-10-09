from ..utils.db import db

class Citizen(db.Model):
    __tablename__= 'citizens'

    id=db.Column(db.Integer(),primary_key=True)
    email=db.Column(db.String(80),nullable=False,unique=True)
    username = db.Column(db.String(25),nullable=False, unique=True)
    first_name = db.Column(db.String(25),nullable=True)
    last_name = db.Column(db.String(25),nullable=True)
    password_hash=db.Column(db.Text(),nullable=False)
    is_sale_opportunity=db.Column(db.Boolean(),default=True)
    cars=db.relationship('Car',backref='car_owner',lazy=True)

    def __repr__(self):
        f"<Citizen {self.id} {self.username}>"


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()