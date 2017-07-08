from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from my_app.models import User
from my_app.schema import UserRegistrationSchema, UserLoginSchema


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request to register a user."""
        print(request.data)

        # Query to check if the user already exists
        user = User.query.filter_by(username=request.data['username']).first()
        existing_email = User.query.filter_by(email=request.data['email']).first()
        if user:
            response = {
                'message': 'The username has been taken.'
            }
            return make_response(jsonify(response)), 409
        elif existing_email:
            response = {
                'message': 'The email exists please login.'
            }
            return make_response(jsonify(response)), 409

        else:
            post_data = request.data
            registration_schema = UserRegistrationSchema()
            errors = registration_schema.validate(post_data)
            if errors:
                return errors
            try:
                username = post_data['username']
                email = post_data['email']
                password = post_data['password']
                user = User(username=username, email=email, password=password)
                user.save()
                user_details = {"username": post_data['username'],
                                            "email":  post_data['email'],
                                            "password": post_data['password'],
                                            "id": user.id
                                             }
                response = {
                    'message': 'You registered successfully!'
                }
                response.update(user_details)

                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401


class LoginView(MethodView):
    """This view handles user login and access token generation."""

    def post(self):
        """Handle POST request for login view."""
        try:
            post_data = request.data
            login_schema = UserLoginSchema()
            errors = login_schema.validate(post_data)
            if errors:
                return errors
            user = User.query.filter_by(username=post_data['username']).first()
            # Authenticate the user using their password
            if user and user.password_is_valid(post_data['password']):
                # Generate the access token.
                access_token = str(user.generate_token(user.id, app=auth_blueprint))
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token
                            }
                    return make_response(jsonify(response)), 200
                else:
                    response = {
                        'message': 'Invalid token!'
                            }
                    return make_response(jsonify(response)), 401
            else:
                response = {
                    'message': 'Invalid username or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

# Define the API resources
registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

# Define the rule for the urls and then add the rule to the blueprint.
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST'])
