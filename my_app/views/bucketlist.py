from flask.views import MethodView
from flask import request, jsonify, abort, make_response



#from decorator import login_required

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

            bucketlist = Bucketlist(name=name)
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'created_by': bucketlist.created_by,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response = {"message": "Bucketlist created successfully."}
            return make_response(jsonify(response)), 201

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
    def put(self,id):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)
            response = {"message": "The bucketlist does not exist."}
            return make_response(jsonify(response)), 404
        else:
            name = str(request.data.get('name'))

class BucketListView(MethodView):
    #decorators = [login_required]

    def bucketlists():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                bucketlist = Bucketlist(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'created_by': bucketlist.created_by,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201
                return response
        else:
            bucketlists = Bucketlist.get_all()
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    def bucketlist_manipulation(id, **kwargs):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)
            return make_response(jsonify(response)), 404

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
            "message": "bucketlist {} deleted successfully".format(bucketlist.id)
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })

            response = {"message": "Bucketlist updated successfully."}
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
    methods=['DELETE', 'PUT'])
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response

#  # API resource
# bucketlist_view = BucketListView.as_view("bucketlist_view")
# manipulation_view = BucketListManipulationView.as_view("manipulation_view")

# # Rule for bucketlist with blueprint
# bucketlist_blueprint.add_url_rule("/bucketlists/", view_func=bucketlist_view,
#                                   methods=["POST", "GET"])
# bucketlist_blueprint.add_url_rule(
#     "/bucketlists/<int:id>/", view_func=manipulation_view,
#     methods=["PUT", "GET", "DELETE"])
