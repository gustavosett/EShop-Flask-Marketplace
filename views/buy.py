from flask import Blueprint, flash, redirect, render_template, session, url_for
from utils import get_user_cart_and_wishlist
from flask_login import current_user
from database import get_db
from models import Product, ProductInfo, Cart, CartItem
from sqlalchemy.orm import joinedload, subqueryload


buy = Blueprint('buy', __name__)


@buy.route('/cart', methods=['GET', 'POST'])
def my_cart():
    if not current_user.is_authenticated:
        flash('you need to be logged')
        return redirect(url_for('auth.login'))
    user_id = current_user.id
    with get_db() as db_session:
        cart = (
            db_session.query(Cart)
            .filter(Cart.user_id == user_id)
            .options(
                joinedload(Cart.items).joinedload(CartItem.product),
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.product_info).joinedload(ProductInfo.user),
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.product_pictures)
            )
            .first()
        )
        cart.items
        print(cart.__dict__)
    data = get_user_cart_and_wishlist(user_id)
    return render_template('cart.html', cart=cart, data=data)

