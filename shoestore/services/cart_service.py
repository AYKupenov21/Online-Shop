# carts: dict mapping user_email -> list of items
# item: {product_id, quantity, size}
from services.catalog_service import CatalogService

_CARTS = {}
catalog = CatalogService()

class CartService:
    def get_cart(self, user_email):
        return _CARTS.get(user_email, [])

    def add_item(self, user_email, product_id, qty=1, size=None):
        p = catalog.get(product_id)
        if not p:
            return False, "Продуктът не е намерен."
        if p["stock"] < qty:
            return False, "Няма достатъчна наличност."
        item = {"product_id": product_id, "quantity": qty, "size": size, "product": p}
        _CARTS.setdefault(user_email, []).append(item)
        return True, "OK"

    def remove_item(self, user_email, product_id):
        items = _CARTS.get(user_email, [])
        _CARTS[user_email] = [i for i in items if i["product_id"] != product_id]
        return True

    def clear_cart(self, user_email):
        _CARTS[user_email] = []
        return True
