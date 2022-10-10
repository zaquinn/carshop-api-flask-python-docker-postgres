import http
from flask_restx import Namespace,Resource,fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from http import HTTPStatus
from ..utils.db import db
from ..models.citizens import Citizen
from werkzeug.security import generate_password_hash

car_namespace=Namespace('cars',description="Namespace for cars")

car_model=car_namespace.model(
    'Car',{
        'id':fields.Integer(description="An ID"),
        'model':fields.String(description="A car model"),
        'brand':fields.String(description="A car brand"),
        'color':fields.String(description="The car color",default="Not Specified",
            enum=['Yellow','Blue','Gray','Not Specified']
        ),
        'car_type':fields.String(description="The car type",
            default="Not Specified", enum=['Hatch','Sedan','Convertible','Not Specified']
        )
    }
)

citizen_namespace=Namespace('citizens',description="Namespace for citizens")

citizen_model=citizen_namespace.model(
    'Citizen',{
        'id':fields.Integer(description="An ID"),
        'email':fields.String(description="An email"),
        'username':fields.String(description="A username"),
        'first_name':fields.String(description="A first name"),
        'last_name':fields.String(description="A last name"),
        'cars':fields.List(fields.Nested(car_model)),
        'is_sale_opportunity':fields.Boolean(description="Says if a citizen is a sale opportunity",default=True)
    }
)


@citizen_namespace.route('/citizen/<int:citizen_id>')
class GetUpdateDelete(Resource):

    @citizen_namespace.marshal_with(citizen_model)
    @citizen_namespace.doc(
        description="Retrieve an citizen by ID",
        params={
            "citizen_id":"An ID for a given citizen"
        }
    )
    @jwt_required()
    def get(self,citizen_id):
        """
            Retrieve an citizen by its id
        """
        citizen=Citizen.get_by_id(citizen_id)


        return citizen ,HTTPStatus.OK
    
    @citizen_namespace.expect(citizen_model)
    @citizen_namespace.marshal_with(citizen_model)
    @citizen_namespace.doc(
        description="Update an citizen given an citizen ID",
        params={
            "citizen_id":"An ID for a given citizen"
        }
    )
    @jwt_required()
    def patch(self,citizen_id):

        """
            Update an citizen with id
        """
        

        citizen_to_update=Citizen.get_by_id(citizen_id)

        data=citizen_namespace.payload

        citizen_to_update.email=data('email', citizen_to_update.email)
        citizen_to_update.username=data('username', citizen_to_update.username)
        citizen_to_update.first_name=data('first_name', citizen_to_update.first_name)
        citizen_to_update.last_name=data('last_name', citizen_to_update.last_name)
        if data.get('password'):
            citizen_to_update.password_hash=generate_password_hash(data['password'])
            

        citizen_to_update_return = {
                "message": "User updated with success",
                "updated": {
                "username": citizen_to_update.username,
                "email": citizen_to_update.email,
                "first_name": citizen_to_update.first_name,
                "last_name": citizen_to_update.last_name,
                "cars": citizen_to_update.cars
                }
            }

        db.session.commit()

        return citizen_to_update_return, HTTPStatus.OK



    @jwt_required()
    @citizen_namespace.marshal_with(citizen_model)
    @citizen_namespace.doc(
        description="Delete an citizen given an citizen ID",
        params={
            "citizen_id":"An ID for a given citizen"
        }
    )
    def delete(self,citizen_id):

        """
            Delete an citizen with id
        """
        citizen_to_delete=Citizen.get_by_id(citizen_id)

        citizen_to_delete.delete()

        return citizen_to_delete ,HTTPStatus.NO_CONTENT
