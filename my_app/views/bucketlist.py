from flask.views import MethodView
from decorator import login_required
from . import bucketlist_blueprint
from flask import request, jsonify, abort, make_response
from my_app.models import Bucketlist, BucketlistItem
from my_app.schema import BucketlistSchema


class BucketlistView(MethodView):
    decorators = [login_required]

    def post(self, user_id):
        name = str(request.data.get('name', ''))
        data = request.data
        if name:
            bucketlist_schema = BucketlistSchema()
            errors = bucketlist_schema.validate(data)
            if errors:
                return errors
            existing_bucketlist = Bucketlist.query.filter_by(
                name=name, created_by=user_id).first()
            if existing_bucketlist:
                response = {"message": "The bucketlist already exists!"}
                return make_response(jsonify(response)), 409

            else:
                bucketlist = Bucketlist(name=name)
                bucketlist.save()
                response = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'created_by': bucketlist.created_by,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                    'items': bucketlist.items
                }
                response.update(
                    {"message": "Bucketlist created successfully!"})
                return make_response(jsonify(response)), 201
        else:
            response = {"message": "Bucketlist name should be provided."}
            return make_response(jsonify(response)), 400

    def get(self, user_id):
            bucketlists = Bucketlist.query.filter_by(
                created_by=user_id).first()
            if not bucketlists:
                response = {"message": "You do not have any bucketlists."}
                return make_response(jsonify(response)), 404
            else:
                results = []
                itemslist = []
                for bucketlist in bucketlists:
                    items = BucketlistItem.query.filter_by(
                        bucketlist_id=bucketlist.id).all()
                    for item in items:
                        itemdict = {
                            'id': item.id,
                            'name': item.name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'done': item.done}
                        itemslist.append(itemdict)

                    obj = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'items': itemslist
                    }
                    itemslist = []
                    results.append(obj)
                return make_response(jsonify(results)), 200


class BucketlistManipulationView(MethodView):
    decorators = [login_required]

    def get(self, id, user_id):
        bucketlists = Bucketlist.query.filter_by(
            created_by=user_id).all()
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlists:
            response = {"message": "You do not have any bucketlists."}
            return make_response(jsonify(response)), 404
        else:
            itemslist = []
            try:
                the_bucketlist = [bucketlist for bucketlist in bucketlists if bucketlist.id==id][0]
                items = BucketlistItem.query.filter_by(
                    bucketlist_id=bucketlist.id).all()
                for item in items:
                    itemdict = {
                        'id': item.id,
                        'name': item.name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified,
                        'done': item.done}
                    itemslist.append(itemdict)
                response = {
                    'id': the_bucketlist.id,
                    'name': the_bucketlist.name,
                    'date_created': the_bucketlist.date_created,
                    'date_modified': the_bucketlist.date_modified,
                    'items': itemslist
                }
                return make_response(jsonify(response)), 200
            except IndexError:
                response = {"message": "The bucketlist does not exist."}
                return make_response(jsonify(response)), 404

    def put(self, id, user_id):
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            abort(404)
            response = {"message": "The bucketlist does not exist."}
            return make_response(jsonify(response)), 404
        else:
            name = str(request.data.get('name'))
            if name == bucketlist.name:
                response = {"message": "The bucketlist cannot\
 be updated with the same data."}
                return make_response(jsonify(response)), 409
            else:
                bucketlist.name = name
                bucketlist.save()
                response = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                }
                response.update(
                    {"message": "Bucketlist updated successfully."})
                return make_response(jsonify(response)), 200

    def delete(self, id, user_id):
        bucketlists = Bucketlist.query.filter_by(
            created_by=user_id).all()
        try:
            bucketlist = [bucketlist for bucketlist in bucketlists if bucketlist.id == id][0]
            bucketlist.delete()
            response = {"message": "Bucketlist deleted successfully."}
            return make_response(jsonify(response)), 200
        except IndexError:
            response = {"message": "The bucketlist does not exist."}
            return make_response(jsonify(response)), 404

# API resource
bucketlist_view = BucketlistView.as_view("bucketlist_view")
manipulation_view = BucketlistManipulationView.as_view("manipulation_view")

bucketlist_blueprint.add_url_rule("/bucketlists/", view_func=bucketlist_view,
                                  methods=["POST", "GET"])
bucketlist_blueprint.add_url_rule(
    "/bucketlists/<int:id>", view_func=manipulation_view,
    methods=['DELETE', 'GET', 'PUT'])
