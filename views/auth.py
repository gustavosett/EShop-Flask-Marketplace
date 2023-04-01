from flask import Blueprint, render_template, redirect, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models.models import User, Cart, Wishlist
from database import get_db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        with get_db() as db:
            user = db.query(User).filter_by(email=email).first()
            print(user)
            if not user:
                flash('Invalid email.')
                return redirect(url_for('auth.login'))
            elif not check_password_hash(user.password_hash, password):
                flash('wrong password.')
                return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        flash(f'welcome {user.name}!!')
        return redirect(url_for('main.home'))
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role_id = request.form.get('role')
        id_number = request.form.get('id_number')
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        
        password_hash = generate_password_hash(password, method='sha256')

        new_user = User(
            role_id=role_id, 
            id_number=id_number, 
            name=name, 
            last_name=last_name, 
            phone=phone, 
            email=email, 
            password_hash=password_hash
        )
        try:
            with get_db() as session:
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                user_cart = Cart(
                    user_id=new_user.id
                )
                user_wishlist = Wishlist(
                    user_id=new_user.id
                )
                session.add_all([user_cart, user_wishlist])
                session.commit()
                flash('Sucessful! Now login into your account to continue.')
                return redirect(url_for('auth.login'))
        except IntegrityError as e:
            session.rollback()
            flash('invalid data, try again.')
            return redirect(url_for('auth.register'))
    return render_template('register.html')


@auth.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    logout_user()
    if request.method == 'POST':
        id_number = request.form.get('id_number')
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')

        password_hash = generate_password_hash(password, method='sha256')

        new_user = User(
            role_id=1, 
            id_number=id_number, 
            name=name, 
            last_name=last_name, 
            phone=phone, 
            email=email, 
            password_hash=password_hash
        )

        try:
            with get_db() as session:
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                user_cart = Cart(
                    user_id=new_user.id
                )
                user_wishlist = Wishlist(
                    user_id=new_user.id
                )
                session.add_all([user_cart, user_wishlist])
                session.commit()
                flash('Sucessful! Now login into your account to continue.')
                return redirect(url_for('auth.login'))
        except IntegrityError as e:
            session.rollback()
            flash('invalid data, try again.')
            return redirect(url_for('auth.admin_register'))
    return render_template('admin_register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
