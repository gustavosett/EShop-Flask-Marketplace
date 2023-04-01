from typing import List, Tuple
from database import get_db
from sqlalchemy.orm import joinedload, Query
from models import Cart, CartItem, Product, Wishlist, WishlistItem, ProductInfo

def get_user_cart(user_id):
    with get_db() as db:
        user_cart = (
            db.query(Cart)
            .filter(Cart.user_id == user_id)
            .options(
                joinedload(Cart.items).joinedload(CartItem.product),
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.product_info).joinedload(ProductInfo.user),
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.product_pictures)
            )
            .first()
        )
        cart_items = user_cart.items
    if user_cart and cart_items:
        cart_len = sum([item.quantity for item in cart_items])
        cart_total_value = sum([item.quantity * item.unit_value for item in cart_items])
    else:
        cart_len = 0
        cart_total_value = 0

    return {
        "cart": user_cart,
        "cart_items": cart_items,
        "cart_len": cart_len,
        "cart_total_value":cart_total_value
    }

def get_user_wishlist(user_id):
    with get_db() as db:
        user_wishlist = (
            db.query(Wishlist)
            .filter(Wishlist.user_id == user_id)
            .options(
                joinedload(Wishlist.items).joinedload(WishlistItem.product),
                joinedload(Wishlist.items).joinedload(WishlistItem.product).joinedload(Product.product_info).joinedload(ProductInfo.user),
                joinedload(Wishlist.items).joinedload(WishlistItem.product).joinedload(Product.product_pictures)
            )
            .first()
        )
        wishlist_items = user_wishlist.items
        wishlist_len = 0
        wishlist_total_value = 0
    try:
        if user_wishlist and wishlist_items:
            wishlist_len = len(wishlist_items)
            wishlist_total_value = sum([item.value for item in wishlist_items])
    except:
        pass

    return {
        "wishlist": user_wishlist,
        "wishlist_items": wishlist_items,
        "wishlist_len": wishlist_len,
        "wishlist_total_value":wishlist_total_value
    }

def get_user_cart_and_wishlist(user_id):
    user_cart = get_user_cart(user_id)
    user_wishlist = get_user_wishlist(user_id)

    return {
        "cart": user_cart["cart"],
        "cart_items": user_cart["cart_items"],
        "cart_len": user_cart["cart_len"],
        "cart_total_value": user_cart["cart_total_value"],
        "wishlist": user_wishlist["wishlist"],
        "wishlist_items": user_wishlist["wishlist_items"],
        "wishlist_len": user_wishlist["wishlist_len"],
        "wishlist_total_value": user_wishlist["wishlist_total_value"]
    }

# with get_db() as db:
#     user_cart = Cart(id=1, user_id=1, items=[
#         CartItem(id=1, cart_id=1, product_id=1),
#         CartItem(id=2, cart_id=1, product_id=1),
#         CartItem(id=3, cart_id=1, product_id=1)
#     ])
#     if user_cart:
#         cart_items = user_cart.items
#         cart_len = sum([item.quantity for item in cart_items])
#         cart_total_value = sum([item.quantity * item.unit_value for item in cart_items])
#     else:
#         cart_items = []
#         cart_len = 0
#         cart_total_value = 0

#     print (
#         "cart", user_cart,
#         "cart_items", cart_items,
#         "cart_len", cart_len,
#         "cart_total_value",cart_total_value
#     )

#     for item in cart_items:
#         print('teste')
#         print(item.product)