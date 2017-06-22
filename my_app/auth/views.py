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
                response = {
                    'message': 'You registered successfully!'
                }
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

registration_view = RegistrationView.as_view('register_view')
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])