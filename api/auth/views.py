from api.config.config import Config
from flask_restx import Resource,Namespace,fields
from flask import request
from werkzeug.security import generate_password_hash,check_password_hash
from http import HTTPStatus
from flask_jwt_extended import (create_access_token,
create_refresh_token,jwt_required,get_jwt_identity)
from werkzeug.exceptions import Conflict,BadRequest
from ..models.citizens import Citizen

auth_namespace=Namespace('auth',description="a namespace for authentication routes")

signup_model=auth_namespace.model(
    'SignUp',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password"),
    }
)

citizen_model=auth_namespace.model(
    'Citizen',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        "first_name": fields.String(required=False,description="A first name"),
        "last_name": fields.String(required=False,description="A last name"),
    }
)

login_model=auth_namespace.model(
    'Login',{
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password")
    }
)

@auth_namespace.route('/signup')
class SignUp(Resource):
    
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(citizen_model)
    def post(self):
        """
            Create a new citizen account 
        """

        data = request.get_json()
        

        try:

            new_citizen=Citizen(
                username=data.get('username'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password')),
                first_name=data.get("first_name"),
                last_name=data.get("last_name")
            )

            new_citizen_return = {
                "id": new_citizen.id,
                "username": new_citizen.username,
                "email": new_citizen.email,
                "first_name": new_citizen.first_name,
                "last_name": new_citizen.last_name,
                "cars": new_citizen.cars
            }



            new_citizen.save()

            return new_citizen_return , HTTPStatus.CREATED

        except Exception as e:
            if f"{type(e)}" == "<class 'sqlalchemy.exc.IntegrityError'>":
                raise BadRequest({"obrigatory fields": "username, email, password", "optional fields": "first_name, last_name", "alert": "User might be already registered"})
            raise Conflict(f"{e}, type: {type(e)}")


@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate a JWT when successfully logged in
        
        """


        data=request.get_json()


        email=data.get('email')
        password=data.get('password')

        citizen=Citizen.query.filter_by(email=email).first()


        if (citizen is not None) and check_password_hash(citizen.password_hash,password):
            access_token=create_access_token(identity=citizen.username)
            refresh_token=create_refresh_token(identity=citizen.username)

            response={
                'acccess_token':access_token,
                'refresh_token':refresh_token
            }

            return response, HTTPStatus.OK


        raise BadRequest("Invalid Username or password")


@auth_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        username=get_jwt_identity()


        access_token=create_access_token(identity=username)

        return {'access_token':access_token},HTTPStatus.OK