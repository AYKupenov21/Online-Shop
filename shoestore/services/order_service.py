from services.catalog_service import CatalogService
from services.notifier import ConsoleNotifier, Notifier
import uuid
import time
from typing import List, Dict, Any, Optional

_ORDERS: List[Dict[str, Any]] = []

catalog = CatalogService()


class OrderService:
    def __init__(self, notifier: Optional[Notifier] = None, catalog_service: Optional[CatalogService] = None):
        # Allow dependency injection (tests, different notifier implementations, etc.)
        self.notifier = notifier or ConsoleNotifier()
        # keep single catalog instance for module-level usage compatible with previous behavior
        self.catalog = catalog_service or catalog

    def create_order(self, user_email: str, items: List[Dict[str, Any]], address: str, payment_method: str):
        # Reduce stock for each item using catalog.reduce_stock (keeps previous semantics)
        for it in items:
            pid = it["product_id"]
            qty = it["quantity"]
            ok, msg = self.catalog.reduce_stock(pid, qty)
            if not ok:
                return False, f"Failed order: {msg} (product {pid})"

        order = {
            "id": str(uuid.uuid4()),
            "user": user_email,
            "items": items,
            "address": address,
            "payment": payment_method,
            "created_at": time.time()
        }
        _ORDERS.append(order)

        # Use notifier abstraction to simulate sending confirmation
        subject = "Order Confirmation"
        body = f"Order {order['id']} was successful."
        try:
            self.notifier.notify(user_email, subject, body)
        except Exception:
            # Fall back to previous behavior if notifier fails
            print(f"[EMAIL SIMULATION] To: {user_email} | Subject: {subject} | Body: {body}")

        return True, order

    def list_orders(self):
        return list(_ORDERS)
