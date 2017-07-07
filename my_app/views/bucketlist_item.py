from flask.views import MethodView
from flask import request, jsonify, abort, make_response
from my_app.models import Bucketlist, BucketlistItem
from . import bucketlist_item_blueprint
from my_app.schema import BucketlistItemSchema


class BucketlistItemView(MethodView):

    def post(self, id):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            response = {"message": "You do not have any backetlists."}
            return make_response(jsonify(response)), 404
        else:
            name = str(request.data.get('name'))
            data = request.data
            if name:
                item_schema = BucketlistItemSchema()
                errors = item_schema.validate(data)
                if errors:
                    return errors
                existing_item = BucketlistItem.query.filter_by(name=name,).first()
                if existing_item:
                    response = {"message": "The bucketlist item already exists!"}
                    return make_response(jsonify(response)), 409
                else:
                    item = BucketlistItem(name=name, bucketlist_id=id)
                    item.save()
                    response = {
                        'id': item.id,
                        'name': item.name,
                        'date_created': str(item.date_created),
                        'date_modified': str(item.date_modified),
                        'bucketlist_id': bucketlist.id
                    }
                    response.update({"message": "The bucketlist item has been created!"})
                    return make_response(jsonify(response)), 201
            else:
                response = {"message": "Please enter bucketlist item name."}

                return make_response(jsonify(response)), 400

    def get(self, id):
            bucketlist_items = BucketlistItem.query.filter_by(bucketlist_id=id).all()
            if bucketlist_items:
                results = []
                count = 1
                for item in bucketlist_items:
                    obj = {
                        'id': count,
                        'name': item.name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified
                    }
                    results.append(obj)
                    count += 1
                response = jsonify(results)
                return make_response(response), 200
            else:
                response = {"message": "You do not have any bucketlists items."}
                return make_response(jsonify(response)), 404


class BucketlistItemManipulationView(MethodView):
        def put(self, id, item_id):
            item = BucketlistItem.query.filter_by(
                bucketlist_id=id, id=item_id).first()

            if item:
                name = str(request.data.get('name', ''))
                item.name = name
                item.save()
                response = {
                        'id': item.id,
                        'name': item.name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified
                }
                response .update({"message": "Bucketlist item updated successfully."})
                return make_response(jsonify(response)), 200
            else:
                abort(404)
                response = {"message": "The bucketlist does not exist."}
                return make_response(jsonify(response)), 404

        def get(self, id, item_id):
            items = BucketlistItem.query.filter_by(bucketlist_id=id).all()
            item = BucketlistItem.query.filter_by(id=item_id).first()
            the_item = items[int(item_id) - 1]
            #the_item = [item for item in items if item.id == item_id][0]
            if the_item:
                results = {
                    'id':  item_id ,
                    'name': the_item.name,
                    'date_created': the_item.date_created,
                    'date_modified': the_item.date_modified
                }
                response = jsonify(results)
                return make_response(response), 200

            else:
                response = {"message": "You do not have any bucketlists items."}
                return make_response(jsonify(response)), 404

        def delete(self, id, item_id):
            item = BucketlistItem.query.filter_by(bucketlist_id=id, id=item_id).first()
            if item:
                item.delete()
                response = {"message": "Bucketlist item deleted successfully."}
                return make_response(jsonify(response)), 200
            else:
                abort(404)
                response = {"message": "The bucketlist item does not exist."}
                return make_response(jsonify(response)), 404

 # API resource
bucketlist_item_view = BucketlistItemView.as_view("bucketlist_item_view")
manipulation_view = BucketlistItemManipulationView.as_view("manipulation_view")

# Rule for bucketlist with blueprint
bucketlist_item_blueprint.add_url_rule("/bucketlists/<int:id>/items/", view_func=bucketlist_item_view,
                                  methods=["POST", "GET"])
bucketlist_item_blueprint.add_url_rule(
    "/bucketlists/<int:id>/items/<int:item_id>", view_func=manipulation_view,
    methods=["PUT", "GET", "DELETE"])
