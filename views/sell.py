from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from PIL import Image
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database import get_db
from models import Product, ProductPicture, ProductInfo, Tag, ProductTag
from utils import get_user_cart_and_wishlist


sell = Blueprint('sell', __name__)


@sell.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_product():
    with get_db() as db_session:
        tags = db_session.query(Tag).all()
    data = get_user_cart_and_wishlist(current_user.id)

    if request.method == 'POST':
        product_name = request.form['name']
        product_description = request.form['description']
        product_quantity = int(request.form['quantity'])
        product_value = float(request.form['value'])
        in_promotion = 'in_promotion' in request.form
        promotion_value = None
        if in_promotion:
            promotion_value = float(request.form['promotion_value'])

        # create new product
        with get_db() as db_session:
            product = Product(name=product_name, description=product_description)
            db_session.add(product)
            db_session.flush()

            # add pictures
            try:
                uploaded_files = request.files.getlist("file[]")
                cont = 0
                for i, file in enumerate(uploaded_files):
                    if file.filename != '':
                        filename = f"{product.id}-{i}.jpg"
                        filepath = os.path.join('static', 'product_imgs', filename)
                        img = Image.open(file)
                        img = img.crop((0, 0, min(img.size), min(img.size)))
                        img = img.resize((1100, 1100))

                        # check if directory exists and create if necessary
                        os.makedirs(os.path.dirname(filepath), exist_ok=True)

                        img.save(filepath)
                        if cont == 0:
                            picture = ProductPicture(product_id=product.id, image_url=f"/static/product_imgs/{filename}", is_default=True)
                        else:
                            picture = ProductPicture(product_id=product.id, image_url=f"/static/product_imgs/{filename}")
                        cont += 1
                        db_session.add(picture)
            except:
                flash('invalid data, try again.')
                return redirect(url_for('sell.sell_product'))


            # add product info
            product_info = ProductInfo(
                product_id=product.id,
                user_id=current_user.id,
                quantity=product_quantity,
                value=product_value,
                in_promotion=in_promotion,
                promotion_value=promotion_value
            )
            db_session.add(product_info)

            # add product tags
            for tag_id in request.form.getlist('tags'):
                tag = db_session.query(Tag).get(tag_id)
                product_tag = ProductTag(product_id=product.id, tag_id=tag.id)
                db_session.add(product_tag)

            db_session.commit()

            return redirect(url_for(
                'shop.product_detail', 
                id=product.id, 
            ))

    return render_template(
        'sell.html',
        data=data,
        tags=tags
    )
