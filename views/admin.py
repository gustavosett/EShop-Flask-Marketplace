from sqlite3 import IntegrityError
from flask import Blueprint, flash, request, render_template, url_for, redirect
from flask_login import current_user, login_required
from database import get_db
from models import Role, Tag
from utils import get_user_cart_and_wishlist


admin = Blueprint('admin', __name__)


@admin.route('/roles', methods=['GET', 'POST'])
@login_required
def roles():
    data = get_user_cart_and_wishlist(current_user.id)
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')

        new_role = Role(
            id=id,
            name=name
        )

        try:
            with get_db() as session:
                session.add(new_role)
                session.commit()
                flash(f'Sucessful! New role "{name}" created!')
                return redirect(url_for('main.home'))
        except IntegrityError as e:
            session.rollback()
            flash('invalid data, try again.')
            return redirect(url_for('admin.roles'))
    return render_template('role.html', data=data, current_user=current_user)


@admin.route('/tags', methods=['GET', 'POST'])
@login_required
def tags():
    data = get_user_cart_and_wishlist(current_user.id)
    if request.method == 'POST':
        name = request.form.get('name')
        
        new_tag = Tag(
            name=name
        )
        try:
            with get_db() as session:
                session.add(new_tag)
                session.commit()
                flash(f'Sucessful! New tag "{name}" created!')
                return redirect(url_for('admin.tags'))
        except IntegrityError as e:
            session.rollback()
            flash('invalid data, try again.')
            return redirect(url_for('admin.tags'))
    return render_template('tags.html', data=data, current_user=current_user)