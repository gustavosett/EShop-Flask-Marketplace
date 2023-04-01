from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Numeric, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
from flask_login import UserMixin
from database import Base, engine

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(15))

    users = relationship("User", back_populates="role")


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), default=2, index=True)
    id_number = Column(String(30), unique=True)
    name = Column(String(50))
    last_name = Column(String(200))
    phone = Column(String(20), unique=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(128))
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True, index=True)
    balance = Column(Numeric(precision=15, scale=2), default=0)
    last_activity = Column(DateTime, default=datetime.now)

    addresses = relationship('Address', back_populates='user')
    role = relationship('Role', back_populates='users')
    sale_products = relationship('ProductInfo', back_populates='user')
    orders = relationship('Order', back_populates='user_client', foreign_keys='Order.user_id')
    sales = relationship('Order', back_populates='user_seller', foreign_keys='Order.seller_id')
    cart = relationship('Cart', back_populates='user')
    wishlist = relationship('Wishlist', back_populates='user')


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    street = Column(String(100), nullable=True)
    number = Column(String(10), nullable=True)
    complement = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(10), nullable=True)
    is_default = Column(Boolean, default=True, index=True)

    user = relationship('User', back_populates='addresses')


class Coupon(Base):
    __tablename__ = 'coupons'

    id = Column(Integer, primary_key=True)
    code = Column(String(50))
    discount_porcentage = Column(Integer)
    is_active = Column(Boolean, default=True)

    orders = relationship('Order', back_populates='coupon')


class ProductTag(Base):
    __tablename__ = 'product_tags'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)


class ProductInfo(Base):
    __tablename__ = 'product_infos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=0)
    in_promotion = Column(Boolean, default=False)
    value = Column(Numeric(precision=15, scale=2))
    promotion_value = Column(Numeric(precision=15, scale=2), nullable=True)

    user = relationship('User', back_populates='sale_products')
    product = relationship('Product', back_populates='product_info')

    def get_user(self):
        return {
            'id': self.user.id,
            'name': f'{self.user.name} {self.user.last_name}',
            'role_id': self.user.role_id
        }

    def get_saved_price(self):
        saved_price = '0.00' 
        if self.in_promotion:
            desc = 100 - (self.promotion_value / self.value * 100) 
            saved_price = f'{desc:.2f}'
        return saved_price

    def get_full_price(self):
        full_price = float(self.value) + float(self.get_saved_price())
        return f'{full_price:.2f}'


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(1000))

    product_info = relationship('ProductInfo', back_populates='product')
    tags = relationship("Tag", secondary='product_tags', back_populates='products')
    product_pictures = relationship('ProductPicture', back_populates='product')

    


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    products = relationship('Product', secondary='product_tags', back_populates='tags')


class ProductPicture(Base):
    __tablename__ = 'product_pictures'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    image_url = Column(String(200), nullable=False, index=True)
    is_default = Column(Boolean, default=False)

    product = relationship('Product', back_populates='product_pictures')


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    shipping_value = Column(Numeric(precision=5, scale=2), default=0.00)
    subtotal_value = Column(Numeric(precision=15, scale=2), default=0.00)
    total_value = Column(Numeric(precision=15, scale=2), default=0.00)

    items = relationship('CartItem', back_populates='cart')
    user = relationship('User', back_populates='cart')


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    quantity = Column(Integer, default=1)
    unit_value = Column(Numeric(precision=15, scale=2))

    cart = relationship('Cart', back_populates='items')
    product = relationship('Product', backref='cart_items')


class Wishlist(Base):
    __tablename__ = 'wishlists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    items = relationship('WishlistItem', back_populates='wishlist')
    user = relationship('User', back_populates='wishlist')


class WishlistItem(Base):
    __tablename__ = 'wishlist_items'

    id = Column(Integer, primary_key=True)
    wishlist_id = Column(Integer, ForeignKey('wishlists.id'), index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    value = Column(Numeric(precision=15, scale=2))

    wishlist = relationship('Wishlist', back_populates='items')
    product = relationship('Product', backref='wishlist_items')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    seller_id = Column(Integer, ForeignKey('users.id'))
    address_id = Column(Integer, ForeignKey('addresses.id'))
    coupon_id = Column(Integer, ForeignKey('coupons.id'), nullable=True)
    status = Column(Integer, default=0) # 0 = Pending, 1 = Denied, 2 = Incompleted, 3 = Approved, 4 = Sent, 5 = Completed
    created_at = Column(DateTime, default=datetime.now)
    total_value = Column(Numeric(precision=15, scale=2))

    shipping_address = relationship('Address', backref='orders')
    items = relationship('OrderItem', back_populates='order')
    coupon = relationship('Coupon', back_populates='orders')
    user_client = relationship('User', back_populates='orders', foreign_keys=[user_id])
    user_seller = relationship('User', back_populates='sales', foreign_keys=[seller_id])


class OrderItem(Base):
    __tablename__ = 'order_items'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer)
    unit_value = Column(Numeric(precision=15, scale=2))
    total_value = Column(Numeric(precision=15, scale=2))

    order = relationship('Order', back_populates='items')
    order_product = relationship('Product', backref='order_items')


try:
    Base.metadata.create_all(engine)
    if not database_exists(engine.url):
        create_database(engine.url)
except Exception as e:
    print(e)