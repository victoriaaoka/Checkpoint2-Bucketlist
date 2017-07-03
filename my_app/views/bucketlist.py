from flask.views import MethodView
from flask import request, jsonify, abort, make_response

#from decorator import login_required
from my_app.models import Bucketlist, BucketlistItem
from . import bucketlist_blueprint


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