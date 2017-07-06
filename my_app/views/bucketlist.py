from flask.views import MethodView
from flask import request, jsonify, abort, make_response
from my_app.models import Bucketlist, BucketlistItem
from . import bucketlist_blueprint


class BucketlistView(MethodView):

    def post(self):
        name = str(request.data.get('name', ''))
        if name:
            existing_bucketlist = Bucketlist.query.filter_by(name=name,).first()
            if existing_bucketlist:
                response = {"message": "The bucketlist already exists!"}
                return make_response(jsonify(response)), 409

            elif not name.isalpha():
                response = {"message": "Bucketlist name can only be of type string."}
                return make_response(jsonify(response)), 400

            else:
                bucketlist = Bucketlist(name=name)
                bucketlist.save()
                response = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'created_by': bucketlist.created_by,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                response.update({"message": "Bucketlist created successfully!"})
                return make_response(jsonify(response)), 201
        else:
            response = {"message": "Bucketlist name should be provided."}
            return make_response(jsonify(response)), 400

    def get(self):
            bucketlists = Bucketlist.get_all()
            if not bucketlists:
                response = {"message": "You do not have any bucketlists."}
                return make_response(jsonify(response)), 404
            else:
                results = []
                for bucketlist in bucketlists:
                    obj = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified
                    }
                    results.append(obj)
                return make_response(jsonify(results)), 200


class BucketlistManipulationView(MethodView):

    def get(self, id):
        bucketlists = Bucketlist.get_all()
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlists:
            response = {"message": "You do not have any bucketlists."}
            return make_response(jsonify(response)), 404
        else:
            try:
                the_bucketlist = [bucketlist for bucketlist in bucketlists if bucketlist.id==id][0]
                response = {
                    'id': the_bucketlist.id,
                    'name': the_bucketlist.name,
                    'date_created': the_bucketlist.date_created,
                    'date_modified': the_bucketlist.date_modified
                }
                return make_response(jsonify(response)), 200
            except IndexError:
                response = {"message": "The bucketlist does not exist."}
                return make_response(jsonify(response)), 404

    def put(self,id):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)
            response = {"message": "The bucketlist does not exist."}
            return make_response(jsonify(response)), 404
        else:
            name = str(request.data.get('name'))
            if not name.isalpha():
                response = {"message": "Bucketlist name can only be of type string."}
                return make_response(jsonify(response)), 400
            else:
                bucketlist.name = name
                if bucketlist.name==Bucketlist.name:
                    response = {"message": "The bucketlist cannot be updated with the same data."}
                    return make_response(jsonify(response)), 409
                else:
                    bucketlist.save()
                    response = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified
                    }
                    response.update({"message": "Bucketlist updated successfully."})
                    return make_response(jsonify(response)), 200

    def delete(self,id):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if bucketlist:
            bucketlist.delete()
            response = {"message": "Bucketlist deleted successfully."}
            return make_response(jsonify(response)), 200
        else:
            abort(404)
            response = {"message": "The bucketlist does not exist."}
            return make_response(jsonify(response)), 404

 # API resource
bucketlist_view = BucketlistView.as_view("bucketlist_view")
manipulation_view = BucketlistManipulationView.as_view("manipulation_view")

# Rule for bucketlist with blueprint
bucketlist_blueprint.add_url_rule("/bucketlists/", view_func=bucketlist_view,
                                  methods=["POST", "GET"])
bucketlist_blueprint.add_url_rule(
    "/bucketlists/<int:id>", view_func=manipulation_view,
    methods=['DELETE', 'GET', 'PUT'])
