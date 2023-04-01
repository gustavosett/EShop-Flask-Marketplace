from flask import Blueprint, redirect, render_template, session, url_for
from utils import get_user_cart_and_wishlist
from flask_login import current_user
from database import get_db
from models import Product, ProductInfo, User, ProductPicture, ProductTag, Order
from sqlalchemy.orm import joinedload, subqueryload


account = Blueprint('account', __name__)


@account.route('/account', methods=['GET'])
def dashboard():
    with get_db() as db:
        user = db.query(User).filter(User.id == current_user.id).options(joinedload(User.orders), joinedload(User.sales)).first()
        data = get_user_cart_and_wishlist(user.id)
        user_balance = user.balance
        user_orders = user.orders

        if user.role_id == 1:
            user_sales = user.sales
            products_with_low_quantity = db.query(Product).join(ProductInfo).filter(ProductInfo.quantity <= 10, ProductInfo.user_id == user.id).options(joinedload(Product.product_info)).all()
            return render_template('account.html', data=data, balance=user_balance, orders=user_orders, role=user.role_id, sales=user_sales, products=products_with_low_quantity)
        elif user.role_id == 3:
            user_sales = user.sales
            return render_template('account.html', data=data, balance=user_balance, orders=user_orders, role=user.role_id, sales=user_sales)
        return render_template('account.html', data=data, balance=user_balance, orders=user_orders, role=user.role_id)

