from flask import Blueprint, render_template, request
from services.catalog_service import CatalogService

catalog_bp = Blueprint("catalog", __name__, template_folder="../templates", url_prefix="/catalog")
catalog_service = CatalogService()

@catalog_bp.route("/")
def view_catalog():
    # Safely read query parameters
    q = request.args.get("q", "")
    q = q.strip() if q else ""

    color = request.args.get("color", "")
    color = color.strip() if color else ""

    shoe_type = request.args.get("shoe_type", "")
    shoe_type = shoe_type.strip() if shoe_type else ""

    size = request.args.get("size", "")
    size = size.strip() if size else ""

    min_price = request.args.get("min_price")
    min_price = float(min_price) if min_price else None

    max_price = request.args.get("max_price")
    max_price = float(max_price) if max_price else None

    in_stock = request.args.get("in_stock") == "1"

    filters = {
        "q": q or None,
        "color": color or None,
        "shoe_type": shoe_type or None,
        "size": size or None,
        "min_price": min_price,
        "max_price": max_price,
        "in_stock": in_stock,
    }

    products = catalog_service.search_and_filter(filters)

    return render_template("catalog.html", products=products, filters=filters)
