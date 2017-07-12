from flask.views import MethodView
from decorator import login_required
from . import bucketlist_blueprint
from flask import request, jsonify, abort, make_response
from my_app.models import Bucketlist, BucketlistItem
from my_app.schema import BucketlistSchema


class BucketlistView(MethodView):
    """
    This class creates a new bucketlist using the POST method.
    It also gets all bucketlists using the GET method."""
    decorators = [login_required]

    def post(self, user_id):
        """
       Creates a new bucketlist.
       ---
       tags:
            - The Bucketlist API
       parameters:
         - in: header
           name: access_token
           type: string
           required: true
         - in: formData
           name: name
           type: string
           required: true
       responses:
         201:
           description: New bucketlist created.

        """
        name = str(request.data.get('name', ''))
        data = request.data
        if name:
            bucketlist_schema = BucketlistSchema()
            errors = bucketlist_schema.validate(data)
            if errors:
                return errors, 400
            existing_bucketlist = Bucketlist.query.filter_by(
                name=name, created_by=user_id).first()
            if existing_bucketlist:
                response = {'message': 'The bucketlist already exists!'}
                return make_response(jsonify(response)), 409

            else:
                bucketlist = Bucketlist(name=name, created_by=user_id)
                count = len(Bucketlist.query.filter_by(
                    created_by=user_id).all())
                bucketlist.save()
                response = {
                    'id':  count + 1,
                    'name': bucketlist.name,
                    'created_by': bucketlist.created_by,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                    'items': bucketlist.items

                }
                response.update(
                    {'message': 'Bucketlist created successfully!'})
                return make_response(jsonify(response)), 201
        else:
            response = {'message': 'Bucketlist name should be provided.'}
            return make_response(jsonify(response)), 400

    def get(self, user_id):
        """
       Retrieve all bucketlists.
       ---
       tags:
            - The Bucketlist API
       parameters:
         - in: header
           name: access_token
           type: string
           required: true
       responses:
         200:
           description: Bucketlists retrieved.
        """
        limit = request.args.get("limit", 20)
        page = request.args.get("page", 1)
        q = request.args.get("q", None)

        if q:
            bucketlists = Bucketlist.query.filter(
                Bucketlist.name.ilike("%" + q + "%"))
            if bucketlists.all():
                bucketlists_pagination = bucketlists.paginate(int(page),
                                                      int(limit), False)
                results = []
                count = 1
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
                        'id': count,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'items': itemslist
                    }
                    itemslist = []
                    results.append(obj)
                    count += 1
                return make_response(jsonify(results)), 200
            else:
                response = {'message': 'No bucketlists found.'}
                return make_response(jsonify(response)), 404
        else:
            bucketlists = Bucketlist.query.filter_by(created_by=user_id)
            if not bucketlists.all():
                response = {'message': 'You do not have any bucketlists.'}
                return make_response(jsonify(response)), 404
            else:
                bucketlists_pagination = bucketlists.paginate(int(page),
                    int(limit), False).items
                results = []
                count = 1
                itemslist = []
                for bucketlist in bucketlists_pagination:
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
                        'id': count,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'items': itemslist
                    }
                    itemslist = []
                    results.append(obj)
                    count += 1
                return make_response(jsonify(results)), 200


class BucketlistManipulationView(MethodView):
    decorators = [login_required]

    def get(self, id, user_id):
        """
       Retrieve a single bucketlist.
       ---
       tags:
            - The Bucketlist API
       parameters:
         - in: header
           name: access_token
           type: string
           required: true
         - in: path
           name: id
           type: integer
           required: true
       responses:
         200:
           description: Bucketlist retrieved.
         404:
           description: Bucketlist not found.
        """
        bucketlists = Bucketlist.query.filter_by(created_by=user_id).all()
        if not bucketlists:
            response = {"message": "You do not have any bucketlists."}
            return make_response(jsonify(response)), 404
        else:
            itemslist = []
            try:
                if id > 0:
                    the_bucketlist = bucketlists[int(id)-1]
                    items = BucketlistItem.query.filter_by(
                        bucketlist_id=the_bucketlist.id).all()
                    for item in items:
                        itemdict = {
                            'id': item.id,
                            'name': item.name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'done': item.done}
                        itemslist.append(itemdict)
                    response = {
                        'id': id,
                        'name': the_bucketlist.name,
                        'date_created': the_bucketlist.date_created,
                        'date_modified': the_bucketlist.date_modified,
                        'items': itemslist
                    }
                    return make_response(jsonify(response)), 200
                else:
                    response = {"message": "Invalid id.{}".format(id)}
                    return make_response(jsonify(response)), 404
            except IndexError:
                response = {"message": "The bucketlist does not exist."}
                return make_response(jsonify(response)), 404

    def put(self, id, user_id):
        """
       Update a bucketlist.
       ---
       tags:
            - The Bucketlist API
       parameters:
         - in: header
           name: access_token
           type: string
           required: true
         - in: path
           name: id
           type: string
           required: true
         - in: formData
           name: name
           type: string
           required: true
       responses:
         200:
           description: Bucketlist updated.
        """
        bucketlists = Bucketlist.query.filter_by(created_by=user_id).all()
        if id < 1:
            response = {"message": "Invalid bucketlist_id"}
            return make_response(jsonify(response)), 404
        try:
            bucketlist = bucketlists[id -1 ]
        except IndexError:
            response = {"message": "The bucketlist does not exist."}
            return make_response(jsonify(response)), 404
        name = str(request.data.get('name'))
        if name == bucketlist.name:
            response = {"message": "The bucketlist cannot\
be updated with the same data."}
            return make_response(jsonify(response)), 409
        else:
            bucketlist.name = name
            bucketlist.save()
            response = {
                'id': id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified,
            }
            response.update(
                {"message": "Bucketlist updated successfully."})
            return make_response(jsonify(response)), 200

    def delete(self, id, user_id):
        """
       Deletes a bucketlist.
       ---
       tags:
            - The Bucketlist API
       parameters:
         - in: header
           name: access_token
           type: string
           required: true
         - in: path
           name: id
           type: integer
           required: true
       responses:
         201:
           description: Bucketlist deleted.

        """
        bucketlists = Bucketlist.query.filter_by(created_by=user_id)
        if id < 1:
            response = {"message": "Invalid bucketlist_id"}
            return make_response(jsonify(response)), 404
        try:
            bucketlist = bucketlists[id -1 ]
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
