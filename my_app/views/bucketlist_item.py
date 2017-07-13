from flask.views import MethodView
from decorator import login_required
from . import bucketlist_item_blueprint
from flask import request, jsonify, abort, make_response
from my_app.models import Bucketlist, BucketlistItem
from my_app.schema import BucketlistItemSchema


class BucketlistItemView(MethodView):
    decorators = [login_required]

    def post(self, id, user_id):
        """
       Creates a new bucketlist item.
       ---
       tags:
            - The Bucketlist Items API
       parameters:
         - in: header
           name: access_token
           type: string
           required: true
         - in: formData
           name: name
           type: string
           required: true
         - in: path
           name: id
           type: integer
           required: true
           description: Bucketlist id
       responses:
         201:
           description: New bucketlist item created.

        """
        bucketlists = Bucketlist.query.filter_by(created_by=user_id).all()
        try:
            bucketlist = bucketlists[id - 1]
        except IndexError:
            response = {'message': 'You do not have any bucketlists.'}
            return make_response(jsonify(response)), 404
        if bucketlist:
            name = str(request.data.get('name'))
            data = request.data
            if name:
                item_schema = BucketlistItemSchema()
                errors = item_schema.validate(data)
                if errors:
                    return errors, 400
                existing_item = BucketlistItem.query.filter_by(
                    name=name,).first()
                if existing_item:
                    response = {'message': 'The bucketlist \
item already exists!'}
                    return make_response(jsonify(response)), 409
                else:
                    item = BucketlistItem(
                        name=name, bucketlist_id=bucketlist.id)
                    item.save()
                    items = BucketlistItem.query.filter_by(
                        bucketlist_id=bucketlist.id).all()
                    response = {
                        'id': len(items),
                        'name': item.name,
                        'date_created': str(item.date_created),
                        'date_modified': str(item.date_modified),
                        'bucketlist_id': id
                    }
                    response.update(
                        {'message': 'The bucketlist item has been created!'})
                    return make_response(jsonify(response)), 201
            else:
                response = {"message": "Please enter bucketlist item name."}

                return make_response(jsonify(response)), 400


class BucketlistItemManipulationView(MethodView):
    decorators = [login_required]

    def put(self, id, item_id, user_id):
        """
       Updates a bucketlist item.
       ---
       tags:
            - The Bucketlist Items API
       parameters:
         - in: header
           name: access_token
           type: string
           required: true
         - in: path
           name: id
           type: integer
           required: true
           description: Bucketlist id
         - in: path
           name: item_id
           type: integer
           required: true
         - in: formData
           name: name
           required: required
           type: string
           description: The item cannot be updated with same data.
       responses:
         201:
           description: Bucketlist item updated.

        """
        try:
            bucketlists = Bucketlist.query.filter_by(created_by=user_id).all()
            bucketlist = bucketlists[id - 1]
            items = BucketlistItem.query.filter_by(
                bucketlist_id=bucketlist.id).all()
        except IndexError:
            response = {'message': 'The bucketlist does not exist.'}
            return make_response(jsonify(response)), 404
        try:
            item = items[item_id-1]
            data = request.data
            if item:
                name = str(request.data.get('name', ''))
                item_schema = BucketlistItemSchema()
                errors = item_schema.validate(data)
                if errors:
                    return errors, 400
            if item.name == name:
                response = {'message': 'The bucketlist cannot \
be updated with same data.'}
                return make_response(jsonify(response)), 409
            else:
                item.name = name
                item.save()
                response = {
                        'id': item.id,
                        'name': item.name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified
                }
                response .update({'message': 'Bucketlist item \
updated successfully.'})
                return make_response(jsonify(response)), 200
        except IndexError:
            response = {'message': 'The bucketlist item does not exist.'}
            return make_response(jsonify(response)), 404

    def delete(self, id, item_id, user_id):
        """
       Deletes a bucketlist.
       ---
       tags:
            - The Bucketlist Items API
       parameters:
         - in: header
           name: access_token
           type: string
           required: true
         - in: path
           name: id
           type: integer
           required: true
         - in: path
           name: item_id
           type: integer
           required: true
       responses:
         201:
           description: Bucketlist item deleted.

        """
        bucketlists = Bucketlist.query.filter_by(created_by=user_id).all()
        bucketlist = bucketlists[id - 1]
        items = BucketlistItem.query.filter_by(
            bucketlist_id=bucketlist.id).all()
        try:
            item = items[item_id-1]
            item.delete()
            response = {'message': 'Bucketlist item deleted successfully.'}
            return make_response(jsonify(response)), 200
        except IndexError:
            response = {'message': 'The bucketlist item does not exist.'}
            return make_response(jsonify(response)), 404

# API resource
bucketlist_item_view = BucketlistItemView.as_view('bucketlist_item_view')
manipulation_view = BucketlistItemManipulationView.as_view('manipulation_view')

# Define the rule for the urls and then add the rule to the blueprint.
bucketlist_item_blueprint.add_url_rule(
    '/bucketlists/<int:id>/items/', view_func=bucketlist_item_view,
    methods=['POST'])
bucketlist_item_blueprint.add_url_rule(
    '/bucketlists/<int:id>/items/<int:item_id>', view_func=manipulation_view,
    methods=['PUT', 'DELETE'])
