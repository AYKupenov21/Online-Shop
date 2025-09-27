from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.catalog_service import CatalogService

admin_bp = Blueprint("admin", __name__, template_folder="../templates", url_prefix="/admin")
catalog_service = CatalogService()

def is_admin():
    u = session.get("user")
    return u and u.get("role") == "admin"

@admin_bp.route("/")
def admin_index():
    if not is_admin():
        flash("Достъпът е ограничен до администратори.")
        return redirect(url_for("auth.login"))
    products = catalog_service.get_all()
    return render_template("admin_index.html", products=products)

@admin_bp.route("/create", methods=["GET", "POST"])
def create_product():
    if not is_admin():
        flash("Достъпът е ограничен.")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "color": request.form.get("color"),
            "sizes": [s.strip() for s in request.form.get("sizes","").split(",") if s.strip()],
            "price": float(request.form.get("price") or 0),
            "stock": int(request.form.get("stock") or 0)
        }
        catalog_service.create_product(data)
        flash("Продуктът е създаден.")
        return redirect(url_for("admin.admin_index"))
    return render_template("admin_create.html")

@admin_bp.route("/edit/<product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if not is_admin():
        flash("Достъпът е ограничен.")
        return redirect(url_for("auth.login"))
    product = catalog_service.get(product_id)
    if not product:
        flash("Продуктът не е намерен.")
        return redirect(url_for("admin.admin_index"))
    if request.method == "POST":
        updates = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "color": request.form.get("color"),
            "sizes": [s.strip() for s in request.form.get("sizes","").split(",") if s.strip()],
            "price": float(request.form.get("price") or 0),
            "stock": int(request.form.get("stock") or 0)
        }
        catalog_service.update_product(product_id, updates)
        flash("Продуктът е обновен.")
        return redirect(url_for("admin.admin_index"))
    return render_template("admin_edit.html", product=product)

@admin_bp.route("/delete/<product_id>", methods=["POST"])
def delete_product(product_id):
    if not is_admin():
        flash("Достъпът е ограничен.")
        return redirect(url_for("auth.login"))
    catalog_service.delete_product(product_id)
    flash("Продуктът е изтрит.")
    return redirect(url_for("admin.admin_index"))
