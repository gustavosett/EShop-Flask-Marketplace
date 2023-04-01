from flask import Blueprint, redirect, render_template, session, url_for, request, flash
from utils import get_user_cart_and_wishlist
from flask_login import current_user
from database import get_db
from models import Product, ProductInfo, User, Cart, CartItem, Wishlist, WishlistItem
from sqlalchemy.orm import joinedload, subqueryload


action = Blueprint('action', __name__)


@action.route('/add_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash('you need to be logged')
        return redirect(url_for('auth.login'))
    with get_db() as db:
        user = db.query(User).filter(User.id == current_user.id).first()
        product_info = db.query(ProductInfo).filter(ProductInfo.product_id == product_id).first()
        cart_item = db.query(CartItem).filter(CartItem.product_id == product_id, CartItem.cart_id == user.cart[0].id).first()

        if product_info and product_info.quantity > 0:
            if cart_item:
                cart_item.quantity += 1
                product_info.quantity -= 1
            else:
                if product_info.in_promotion:
                    new_cart_item = CartItem(cart_id=user.cart[0].id, product_id=product_id, quantity=1, unit_value=product_info.promotion_value)
                else:
                    new_cart_item = CartItem(cart_id=user.cart[0].id, product_id=product_id, quantity=1, unit_value=product_info.value)
                product_info.quantity -= 1
                db.add(new_cart_item)
            db.commit()
        else:
            flash('insufficient stock')
    return redirect(request.referrer)

@action.route('/add_wishlist/<int:product_id>', methods=['GET', 'POST'])
def add_to_wishlist(product_id):
    if not current_user.is_authenticated:
        flash('you need to be logged')
        return redirect(url_for('auth.login'))
    with get_db() as db:
        user = db.query(User).filter(User.id == current_user.id).first()
        existing_wishlist_item = db.query(WishlistItem).filter(WishlistItem.wishlist_id == user.wishlist[0].id, WishlistItem.product_id == product_id).first()

        if not existing_wishlist_item:
            new_wishlist_item = WishlistItem(wishlist_id=user.wishlist[0].id, product_id=product_id)
            db.add(new_wishlist_item)
            db.commit()
    return redirect(request.referrer)

@action.route('/decrease_cart/<int:product_id>', methods=['GET', 'POST'])
def decrease_from_cart(product_id):
    if not current_user.is_authenticated:
        flash('you need to be logged')
        return redirect(url_for('auth.login'))
    with get_db() as db:
        user = db.query(User).filter(User.id == current_user.id).first()
        cart_item = db.query(CartItem).filter(CartItem.product_id == product_id, CartItem.cart_id == user.cart[0].id).first()
        product_info = db.query(ProductInfo).filter(ProductInfo.product_id == product_id).first()

        if cart_item:
            cart_item.quantity -= 1
            product_info.quantity += 1

            if cart_item.quantity <= 0:
                db.delete(cart_item)
                flash('deleted!')
            db.commit()
    return redirect(request.referrer)

@action.route('/delete_cart/<int:product_id>', methods=['GET', 'POST'])
def delete_from_cart(product_id):
    if not current_user.is_authenticated:
        flash('you need to be logged')
        return redirect(url_for('auth.login'))
    with get_db() as db:
        user = db.query(User).filter(User.id == current_user.id).first()
        cart_item = db.query(CartItem).filter(CartItem.product_id == product_id, CartItem.cart_id == user.cart[0].id).first()
        product_info = db.query(ProductInfo).filter(ProductInfo.product_id == product_id).first()

        if cart_item:
            product_info.quantity += cart_item.quantity
            db.delete(cart_item)
            db.commit()
            flash('deleted!')
    return redirect(request.referrer)

@action.route('/delete_wishlist/<int:product_id>', methods=['GET', 'POST'])
def delete_from_wishlist(product_id):
    with get_db() as db:
        user = db.query(User).filter(User.id == current_user.id).first()
        wishlist_item = db.query(WishlistItem).filter(WishlistItem.product_id == product_id, WishlistItem.wishlist_id == user.wishlist[0].id).first()

        if wishlist_item:
            db.delete(wishlist_item)
            db.commit()
    return redirect(request.referrer)
