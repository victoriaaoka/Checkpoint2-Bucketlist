from flask.views import MethodView
from flask import request, jsonify, abort, make_response

import decorator
from my_app.models import Bucketlist, BucketlistItem
from . import bucketlist_item_blueprint

def bucketlistitems():
    if request.method == "POST":
        name = str(request.data.get('name', ''))
        if name:
            item = BucketlistItem(name=name)
            item.save()
            response = jsonify({
                'id': item.id,
                'name': item.name,
                'date_created': item.date_created,
                'date_modified': item.date_modified,
                'bucketlist_id': Bucketlist.id
            })
            response.status_code = 201
            return response
    else:
        bucketlist_items = BucketlistItems.get_all()
        results = []

        for item in bucketlist_items:
            obj = {
                'id': item.id,
                'name': item.name,
                'date_created': item.date_created,
                'date_modified': item.date_modified
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

# @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def bucketlist_manipulation(id, **kwargs):
#     bucketlist = Bucketlist.query.filter_by(id=id).first()
#     if not bucketlist:
#         abort(404)
#         return make_response(jsonify(response)), 404

#     if request.method == 'DELETE':
#         bucketlist.delete()
#         return {
#         "message": "bucketlist {} deleted successfully".format(bucketlist.id)
#      }, 200

#     elif request.method == 'PUT':
#         name = str(request.data.get('name', ''))
#         bucketlist.name = name
#         bucketlist.save()
#         response = jsonify({
#             'id': bucketlist.id,
#             'name': bucketlist.name,
#             'date_created': bucketlist.date_created,
#             'date_modified': bucketlist.date_modified
#         })
#         response.status_code = 200
#         return response
#     else:
#         response = jsonify({
#             'id': bucketlist.id,
#             'name': bucketlist.name,
#             'date_created': bucketlist.date_created,
#             'date_modified': bucketlist.date_modified
#         })
#         response.status_code = 200
#         return response