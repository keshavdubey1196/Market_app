from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from config import DATABASE_URI
from dotenv import load_dotenv
import os
from flask_migrate import Migrate


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db = SQLAlchemy()
migrate = Migrate(app, db)


class Products(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(12), nullable=True, unique=True)
    mobilenum = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __init__(self, name, price, barcode, mobilenum, description):
        self.name = name
        self.price = price
        self.barcode = barcode
        self.mobilenum = mobilenum
        self.description = description

    def __str__(self):
        return self.name


# This will create tables and avoid duplication autmatically
def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()


# Intializing the database and the  migrations
init_db(app)


@app.route('/info', methods=["GET"])
def info():
    return jsonify({"message": "Get link is working"}), 200


if __name__ == "__main__":
    app.run()
