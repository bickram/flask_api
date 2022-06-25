from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,help="This is required field")
    parser.add_argument('store_id', type=int, required=True,help="This is required field")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item already exists'}, 400 # something wrong with request
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500 # Internal Server Error
        return item.json(), 201
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': f'Item {name} deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            try:
                item = ItemModel(name, data['price'], data['store_id'])
            except:
                return {'message': 'An error occured inserting teh item'}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {'message': 'An error occured updating the item'}, 500
        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}