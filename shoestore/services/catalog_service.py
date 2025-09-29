import uuid

_PRODUCTS = []

class CatalogService:
    def __init__(self):
        if not _PRODUCTS:
            self.create_product({
                "name": "Sport Runner",
                "description": "Леки спортни обувки",
                "color": "black",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 120.0,
                "stock": 10,
                "image": "images/shoe1.jpeg"
            })
            self.create_product({
                "name": "Classic Leather",
                "description": "Елегантни кожени обувки",
                "color": "black",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 200.0,
                "stock": 5,
                "image": "images/shoe2.jpg"
            })
            self.create_product({
                "name": "Summer Sandal",
                "description": "Удобни сандали за лятото",
                "color": "black",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 60.0,
                "stock": 20,
                "image": "images/shoe3.jpg"
            })
            self.create_product({
                "name": "Red Sport Runner",
                "description": "Леки червени спортни обувки",
                "color": "red",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 129.9,
                "stock": 10,
                "image": "images/shoe4.jpeg"
            })
            self.create_product({
                "name": "Black Shoes",
                "description": "Черни обувки",
                "color": "black",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 209.0,
                "stock": 5,
                "image": "images/shoe5.jpeg"
            })
            self.create_product({
                "name": "White High Shoes",
                "description": "Бели високи обувки",
                "color": "white",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 61.0,
                "stock": 20,
                "image": "images/shoe6.jpg"
            })
            self.create_product({
                "name": "Interesting Shoes",
                "description": "Интересни обувки",
                "color": "yellow",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 140.0,
                "stock": 10,
                "image": "images/shoe7.jpg"
            })
            self.create_product({
                "name": "Modern Shoes",
                "description": "Модерни обувки",
                "color": "white",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 270.0,
                "stock": 5,
                "image": "images/shoe8.jpg"
            })
            self.create_product({
                "name": "Nature Shoes",
                "description": "Природни обувки",
                "color": "green",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 360.0,
                "stock": 20,
                "image": "images/shoe9.jpg"
            })
            self.create_product({
                "name": "Old Money Shoes",
                "description": "Стари пари обувки",
                "color": "brown",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 150.0,
                "stock": 10,
                "image": "images/shoe10.jpeg"
            })


    def create_product(self, data):
        pid = str(uuid.uuid4())
        p = {
            "id": pid,
            "name": data.get("name"),
            "description": data.get("description"),
            "color": data.get("color"),
            "sizes": data.get("sizes", []),
            "price": float(data.get("price", 0)),
            "stock": int(data.get("stock", 0)),
            "image": data.get("image", "images/placeholder.png")
        }
        _PRODUCTS.append(p)
        return p

    def get_all(self):
        return list(_PRODUCTS)

    def get(self, product_id):
        for p in _PRODUCTS:
            if p["id"] == product_id:
                return p
        return None

    def update_product(self, product_id, updates):
        p = self.get(product_id)
        if not p:
            return False
        p.update(updates)
        return True

    def delete_product(self, product_id):
        global _PRODUCTS
        _PRODUCTS = [p for p in _PRODUCTS if p["id"] != product_id]
        return True

    def search_and_filter(self, filters):
        results = _PRODUCTS
        q = filters.get("q") or ""
        color = filters.get("color") or ""
        min_price = filters.get("min_price")
        max_price = filters.get("max_price")
        size = filters.get("size")
        in_stock = filters.get("in_stock")

        if q:
            results = [p for p in results if q.lower() in p["name"].lower() or q.lower() in p["description"].lower()]
        if color:
            results = [p for p in results if color.lower() in p["color"].lower()]
        if min_price is not None:
            results = [p for p in results if p["price"] >= min_price]
        if max_price is not None:
            results = [p for p in results if p["price"] <= max_price]
        if size:
            results = [p for p in results if size in p.get("sizes",[])]
        if in_stock:
            results = [p for p in results if p.get("stock",0) > 0]
        return results

    def reduce_stock(self, product_id, qty):
        p = self.get(product_id)
        if not p:
            return False, "The product does not exist."
        if p["stock"] < qty:
            return False, "There is not enough stock."
        p["stock"] -= qty
        return True, "OK"
