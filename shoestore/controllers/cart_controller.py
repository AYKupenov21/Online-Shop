from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.cart_service import CartService
from services.catalog_service import CatalogService
from services.order_service import OrderService

cart_bp = Blueprint("cart", __name__, template_folder="../templates", url_prefix="/cart")
cart_service = CartService()
catalog_service = CatalogService()
order_service = OrderService()

def current_user_email():
    u = session.get("user")
    return u["email"] if u else None

@cart_bp.route("/")
def view_cart():
    user = current_user_email()
    items = cart_service.get_cart(user)
    return render_template("cart.html", items=items)

@cart_bp.route("/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    user = current_user_email()
    if not user:
        flash("You need to be an admin to access this page.")
        return redirect(url_for("auth.login"))
    qty = int(request.form.get("quantity", 1))
    size = request.form.get("size") or None
    success, msg = cart_service.add_item(user, product_id, qty, size)
    if success:
        flash("The cart item has been added.")
    else:
        flash(msg)
    return redirect(url_for("catalog.view_catalog"))

@cart_bp.route("/remove/<product_id>")
def remove_from_cart(product_id):
    user = current_user_email()
    cart_service.remove_item(user, product_id)
    flash("It has been removed.")
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    user = current_user_email()
    if not user:
        flash("You need to be an admin to access this page.")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        address = request.form.get("address")
        payment = request.form.get("payment")
        items = cart_service.get_cart(user)
        if not items:
            flash("The cart is empty.")
            return redirect(url_for("cart.view_cart"))
        ok, msg = order_service.create_order(user, items, address, payment)
        if ok:
            cart_service.clear_cart(user)
            flash("Your order has been created.")
            return redirect(url_for("catalog.view_catalog"))
        else:
            flash(msg)
    return render_template("checkout.html")
