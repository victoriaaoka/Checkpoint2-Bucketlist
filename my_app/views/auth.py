from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from my_app.models import User

class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request to register a user."""
        print(request.data)

        # Query to check if the user already exists
        user = User.query.filter_by(username=request.data['username']).first()

        if not user:
            try:
                post_data = request.data
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
        else:
            response = {
                'message': 'The user already exists! Please login.'
            }

            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """This view handles user login and access token generation."""

    def post(self):
        """Handle POST request for login view."""
        try:
            user = User.query.filter_by(username=request.data['username']).first()

            # Authenticate the user using their password
            if user and user.password_is_valid(request.data['password']):
                # Generate the access token.
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token
                            }
                    return make_response(jsonify(response)), 200
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
