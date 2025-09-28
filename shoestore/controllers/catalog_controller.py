from flask import Blueprint, render_template, request, session, flash
from services.catalog_service import CatalogService

catalog_bp = Blueprint("catalog", __name__, template_folder="../templates", url_prefix="/catalog")
catalog_service = CatalogService()

@catalog_bp.route("/")
def view_catalog():
    q = request.args.get("q", "").strip()
    color = request.args.get("color", "").strip()
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    size = request.args.get("size")
    in_stock = request.args.get("in_stock")  # "on" or None

    filters = {
        "q": request.args.get("q", "").strip(),
        "color": request.args.get("color", "").strip(),
        "size": request.args.get("size", "").strip(),
        "min_price": float(request.args.get("min_price")) if request.args.get("min_price") else None,
        "max_price": float(request.args.get("max_price")) if request.args.get("max_price") else None,
        "in_stock": request.args.get("in_stock") == "1"
    }
    products = catalog_service.search_and_filter(filters)
    return render_template("catalog.html", products=products, filters=filters)
