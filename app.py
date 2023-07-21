from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
# from flask import jsonify
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


user_products = db.Table('user_products',
                         db.Column('user_id', db.Integer(),
                                   db.ForeignKey('users.id')),
                         db.Column('product_id', db.Integer(),
                                   db.ForeignKey('products.id'))
                         )


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email_address = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False, unique=True)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    products = db.relationship(
        'Product', secondary=user_products, backref='owners')


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


# @app.route('/info', methods=["GET"])
# def info():
#     return jsonify({"message": "Get link is working"}), 200


@app.route('/home')
def home_page():
    products = Products.query.all()
    return render_template('home.html', products=products)


@app.route('/market')
def market_page():
    render_template('market.html')


if __name__ == "__main__":
    app.run()
