from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from utils import get_user_cart_and_wishlist
from flask_login import current_user
from database import get_db
from models import Product, ProductInfo, Cart, CartItem, Order, OrderItem, Address, User
from sqlalchemy.orm import joinedload, subqueryload


checkout = Blueprint('checkout', __name__)


@checkout.route('/checkout', methods=['GET', 'POST'])
def check_out():
    user_id = current_user.id
    data = get_user_cart_and_wishlist(user_id)
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
        products = cart.items
        cart.total_value = 0
        for item in products:
            for i in range(item.quantity):
                cart.total_value += item.unit_value
        db_session.commit()
        if not cart.items:
            flash('no items to buy.')
            return redirect(url_for('main.home'))
        if request.method == 'POST':
            try:
                address = request.form.get('address')
                city = request.form.get('city')
                state = request.form.get('state')
                country = request.form.get('country')
                endereco = Address(
                    user_id=user_id,
                    street=address,
                    city=city,
                    state=state
                )
                db_session.add(endereco)
                db_session.commit()
                db_session.refresh(endereco)
                seller_id = products[0].product.product_info[0].user.id
                ordem = Order(
                    user_id = user_id,
                    seller_id = seller_id,
                    address_id = endereco.id,
                    total_value = cart.total_value
                )
                db_session.add(ordem)
                db_session.commit()
                db_session.refresh(ordem)

                order_items = []
                for item in cart.items:
                    temporary = OrderItem(
                        order_id = ordem.id,
                        product_id = item.product.id,
                        quantity = item.quantity,
                        unit_value = item.unit_value,
                        total_value = (item.unit_value * item.quantity)
                    )
                    order_items.append(temporary)
                    db_session.delete(item)

                db_session.add_all(order_items)
                db_session.commit()
            except:
                db_session.rollback()
                redirect(request.referrer)
            else:
                seller = db_session.query(User).filter(User.id == seller_id).first()
                seller.balance += ordem.total_value
                db_session.commit()
                return render_template('success.html', data=data)
    return render_template('checkout.html', products=products, data=data)