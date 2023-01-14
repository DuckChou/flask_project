from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"item deleted"}

    # 更新item 需要name和price
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self, item_data, item_id):
        # item_data = request.get_json()

        # There's  more validation to do here!
        # Like making sure price is a number, and also both items are optional
        # Difficult to do with an if statement...

        # if "price" not in item_data or "name" not in item_data:
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        #     )

        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id,**item_data)
        
        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()


    # post方法要求请求的json里必须有price,store_id,name
    # 用marshmallow schema来检验输入数据类型和要求
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,item_data):
        # item_data = request.get_json()

        # Here not only we need to validate data exists,
        # But also what type of data. Price should be a float,
        # for example.

        # if (
        #     "price" not in item_data
        #     or "store_id" not in item_data
        #     or "name" not in item_data
        # ):
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
        #     )

        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A store name already exists")
        except SQLAlchemyError:
            abort(500,message="An Error occured while inserting item")

        return item