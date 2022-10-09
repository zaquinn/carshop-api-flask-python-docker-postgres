import http
from flask_restx import Namespace,Resource,fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from http import HTTPStatus
from ..utils.db import db
from ..models.cars import Car
from ..models.citizens import Citizen
from werkzeug.exceptions import BadRequest

car_namespace=Namespace('cars',description="Namespace for cars")

car_model=car_namespace.model(
    'Car',{
        'id':fields.Integer(description="An ID"),
        'color':fields.String(description="The car color",required=True,
            enum=['Yellow','Blue','Gray','Not Specified']
        ),
        'car_type':fields.String(description="The car type",
            required=True, enum=['Hatch','Sedan','Convertible','Not Specified']
        )
    }
)

car_type_model=car_namespace.model(
    'CarType',{
        'car_type':fields.String(description="Car type",
        enums=['Hatch','Sedan','Convertible','Not Specified'])
    }
)

car_color_model=car_namespace.model(
    'Color',{
        'color':fields.String(description="The car color",
        enums=['Yellow','Blue','Gray','Not Specified'])
    }
)

@car_namespace.route('/cars/')
class CarGetCreate(Resource):

    @car_namespace.marshal_with(car_model)
    @car_namespace.doc(
        description="Retrieve all cars"
    )
    @jwt_required()
    def get(self):
        """
            Get all cars
        """
        cars=Car.query.all()

        return cars ,HTTPStatus.OK

    @car_namespace.expect(car_model)
    @car_namespace.marshal_with(car_model)
    @car_namespace.doc(
        description="Register a car"
    )
    @jwt_required()
    def post(self):
        """
            Register a car
        """

        username=get_jwt_identity()

        current_user=Citizen.query.filter_by(username=username).first()

        if len(current_user.cars) >= 3:
            raise BadRequest("A citizen can't have more than three cars")

        data=car_namespace.payload

        new_car=Car(
            model=data['model'],
            brand=data['brand'],
            color=data['color'],
            car_type = data['car_type']
        )

        new_car.car_owner=current_user

        new_car.save()

        return new_car, HTTPStatus.CREATED

@car_namespace.route('/car/<int:car_id>')
class GetUpdateDelete(Resource):

    @car_namespace.marshal_with(car_model)
    @car_namespace.doc(
        description="Retrieve an car by ID",
        params={
            "car_id":"An ID for a given car"
        }
    )
    @jwt_required()
    def get(self,car_id):
        """
            Retrieve an car by its id
        """
        car=Car.get_by_id(car_id)


        return car ,HTTPStatus.OK
    
    @car_namespace.expect(car_model)
    @car_namespace.marshal_with(car_model)
    @car_namespace.doc(
        description="Update an car given an car ID",
        params={
            "car_id":"An ID for a given car"
        }
    )
    @jwt_required()
    def put(self,car_id):

        """
            Update an car with id
        """
        

        car_to_update=Car.get_by_id(car_id)

        data=car_namespace.payload

        car_to_update.model=data['model']
        car_to_update.brand=data['brand']
        car_to_update.color=data['color']
        car_to_update.car_type=data['car_type']

        db.session.commit()

        return car_to_update, HTTPStatus.OK



    @jwt_required()
    @car_namespace.marshal_with(car_model)
    @car_namespace.doc(
        description="Delete an car given an car ID",
        params={
            "car_id":"An ID for a given car"
        }
    )
    def delete(self,car_id):

        """
            Delete an car with id
        """
        car_to_delete=Car.get_by_id(car_id)

        car_to_delete.delete()

        return car_to_delete ,HTTPStatus.NO_CONTENT
