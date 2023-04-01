from flask import Blueprint, redirect, render_template, session, url_for
from utils import get_user_cart_and_wishlist
from flask_login import current_user
from database import get_db
from models import Product, ProductInfo, User, ProductPicture, ProductTag
from sqlalchemy.orm import joinedload, subqueryload


main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    with get_db() as db_session:
        is_adm = False
        if current_user.is_authenticated:
            user = db_session.query(User).filter(User.id == current_user.id).first()
            if user.role_id == 1:
                is_adm = True
                products = (
                    db_session.query(Product)
                    .join(ProductInfo)
                    .join(User, ProductInfo.user_id == User.id)
                    .filter(User.role_id == 3)
                    .options(
                        joinedload(Product.product_info).subqueryload(ProductInfo.user),
                        joinedload(Product.tags),
                        joinedload(Product.product_pictures),
                    )
                    .all()
                )
        if not is_adm:
            products = (
                db_session.query(Product)
                .join(ProductInfo)
                .join(User, ProductInfo.user_id == User.id)
                .filter(User.role_id == 1)
                .options(
                    joinedload(Product.product_info).subqueryload(ProductInfo.user),
                    joinedload(Product.tags),
                    joinedload(Product.product_pictures),
                )
                .all()
            )
    try:
        if current_user.is_authenticated:
            data = get_user_cart_and_wishlist(current_user.id)
            return render_template("home.html", data=data, current_user=current_user, products=products)
    except:
        return redirect(url_for('errors.internal_server_error'))
    return render_template("home.html", products=products)
    

@main.route('/about', methods=['GET'])
def about():
    try:
        if current_user.is_authenticated:
            data = get_user_cart_and_wishlist(current_user.id)
            return render_template("about.html", data=data, current_user=current_user)
    except:
        pass
    return render_template('about.html', current_user=current_user)