from db import db




# 此处把sql表的一个row mapping成了python的一个类 即ItemModel
# 一对多关系: 每个Item只能属于一个Store，一个Store可以有多个Item

class ItemModel(db.Model):
    # 告诉sqlalchemy 表的名字叫做items
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    # 外键 一对多
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id"), unique=False, nullable= False)

    store = db.relationship("StoreModel", back_populates="items")