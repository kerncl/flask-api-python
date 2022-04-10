from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',  # parser will take in this argument in data
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')
    parser.add_argument('store_id',  # parser will take in this argument in data
                        type=int,
                        required=True,
                        help='Every item needs a store id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists"}, 400  # Bad request

        data = self.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting this item with {e}"}, 500 # Internal Server Error

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()
        # data = request.get_json()

        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        # list(map(lambda x: x.json(), ItemModel.query.all()))
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
