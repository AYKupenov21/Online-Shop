from services.catalog_service import CatalogService
import uuid
import time

_ORDERS = []
catalog = CatalogService()

class OrderService:
    def create_order(self, user_email, items, address, payment_method):
        # Пробваме да намалим наличността за всеки артикул
        # Ако някой не може -> връщаме грешка
        for it in items:
            pid = it["product_id"]
            qty = it["quantity"]
            ok, msg = catalog.reduce_stock(pid, qty)
            if not ok:
                return False, f"Неуспешна поръчка: {msg} (продукт {pid})"
        order = {
            "id": str(uuid.uuid4()),
            "user": user_email,
            "items": items,
            "address": address,
            "payment": payment_method,
            "created_at": time.time()
        }
        _ORDERS.append(order)
        # "Изпращане" на имейл (конзола)
        print(f"[EMAIL SIMULATION] To: {user_email} | Subject: Order Confirmation | Body: Поръчка {order['id']} успешно създадена.")
        return True, order

    def list_orders(self):
        return list(_ORDERS)
