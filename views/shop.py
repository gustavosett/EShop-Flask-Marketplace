from flask import Blueprint, redirect, render_template, url_for
from utils import get_user_cart_and_wishlist
from flask_login import current_user, login_required
from database import get_db
from models import Product, ProductInfo, ProductPicture, User
from sqlalchemy.orm import joinedload, subqueryload


shop = Blueprint('shop', __name__)


@shop.route('/shop', methods=['GET'])
def shop_view():
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
            return render_template("shop.html", data=data, current_user=current_user, products=products)
    except:
        return redirect(url_for('errors.internal_server_error'))
    return render_template("shop.html", products=products)
    

@shop.route('/product/<int:id>', methods=['GET'])
def product_detail(id):
    if current_user.is_authenticated:
        data = get_user_cart_and_wishlist(current_user.id)
    with get_db() as db_session:
        product = db_session.query(Product).get(id)
        product_info = db_session.query(ProductInfo).filter_by(product_id=id).first()
        default_picture = db_session.query(ProductPicture).filter_by(product_id=id).first()
        pictures = db_session.query(ProductPicture).filter(
            ProductPicture.product_id == id,
            ProductPicture.id != default_picture.id
        ).all()
        save_price = '0'
        if product_info.in_promotion:
            desc = 100 - (product_info.promotion_value / product_info.value * 100)
            save_price = f'{desc:.2f}'
    if current_user.is_authenticated:   
        return render_template(
            'product.html', 
            data=data, 
            product=product, 
            product_info=product_info, 
            default_picture=default_picture,
            pictures=pictures,
            save_price=save_price
        )
    return render_template(
            'product.html', 
            product=product, 
            product_info=product_info, 
            default_picture=default_picture,
            pictures=pictures,
            save_price=save_price
        )