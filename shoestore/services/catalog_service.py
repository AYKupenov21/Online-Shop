import uuid
from typing import List, Dict, Any, Optional

_PRODUCTS: List[Dict[str, Any]] = []

from services.search import LinearSearch, SearchStrategy
from services.sort import QuickSortByPrice, SortStrategy


class CatalogService:

    def __init__(self, search_strategy: Optional[SearchStrategy] = None, sort_strategy: Optional[SortStrategy] = None):
        self.search_strategy = search_strategy or LinearSearch()
        self.sort_strategy = sort_strategy

        if not _PRODUCTS:
            self.create_product({
                "name": "Sport Runner",
                "description": "Леки спортни обувки",
                "color": "red",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 120.0,
                "stock": 10,
                "image": "images/shoe1.jpeg",
                "shoe_type":"sports"
            })
            self.create_product({
                "name": "Classic Leather",
                "description": "Елегантни кожени обувки",
                "color": "black",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 200.0,
                "stock": 5,
                "image": "images/shoe2.jpg",
                "shoe_type":"classic"
            })
            self.create_product({
                "name": "Modern White Shoes",
                "description": "Модерни бели обувки",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 60.0,
                "stock": 20,
                "image": "images/shoe3.jpg",
                "shoe_type":"modern"
            })
            self.create_product({
                "name": "Modern Vision Brown Shoes With Branded Laces",
                "description": "Кафеви обувки с брандирани връзки",
                "color": "brown",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 129.9,
                "stock": 10,
                "image": "images/shoe4.jpeg",
                "shoe_type":"modern"
            })
            self.create_product({
                "name": "Official Italian Flag Shoes",
                "description": "Обувки с Италианския флаг",
                "color": "white",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 209.0,
                "stock": 5,
                "image": "images/shoe5.jpeg",
                "shoe_type":"official"
            })
            self.create_product({
                "name": "Official Red&White Shoes",
                "description": "Червено-бели обувки",
                "color": "white",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 61.0,
                "stock": 20,
                "image": "images/shoe6.jpg",
                "shoe_type":"official"
            })
            self.create_product({
                "name": "Multiple Logos Grey Shoes",
                "description": "Обувки с много лога",
                "color": "grey",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 140.0,
                "stock": 10,
                "image": "images/shoe7.jpg",
                "shoe_type":"official"
            })
            self.create_product({
                "name": "Basic Grey Shoes",
                "description": "Обикновени сиви обувки",
                "color": "grey",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 270.0,
                "stock": 5,
                "image": "images/shoe8.jpg",
                "shoe_type":"official"
            })
            self.create_product({
                "name": "Big Blue Shoes",
                "description": "Големи сини обувки",
                "color": "blue",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 360.0,
                "stock": 20,
                "image": "images/shoe9.jpg",
                "shoe_type":"modern"
            })
            self.create_product({
                "name": "Clean Black Shoes",
                "description": "Изчистени черни обувки",
                "color": "black",
                "sizes": ["38","39", "40", "41", "42" , "43", "44", "45"],
                "price": 150.0,
                "stock": 10,
                "image": "images/shoe10.jpeg",
                "shoe_type":"official"
            })
            self.create_product({
                "name": "Gold and Black Slides",
                "description": "Черни чехли с златно лого",
                "color": "black",
                "sizes": ["38", "39", "40", "41", "42", "43", "44", "45"],
                "price": 151.0,
                "stock": 10,
                "image": "images/shoe11.jpg",
                "shoe_type": "slides"
            })
            self.create_product({
                "name": "Gold and Black Slides + Italy flag",
                "description": "Черни чехли с златно лого и Италианското знаме",
                "color": "black",
                "sizes": ["38", "39", "40", "41", "42", "43", "44", "45"],
                "price": 152.0,
                "stock": 10,
                "image": "images/shoe12.jpg",
                "shoe_type": "slides"
            })
            self.create_product({
                "name": "Red and Black Slides",
                "description": "Черни чехли с червено лого",
                "color": "black",
                "sizes": ["38", "39", "40", "41", "42", "43", "44", "45"],
                "price": 153.0,
                "stock": 10,
                "image": "images/shoe13.jpg",
                "shoe_type": "slides"
            })

    def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pid = str(uuid.uuid4())
        p = {
            "id": pid,
            "name": data.get("name"),
            "description": data.get("description"),
            "color": data.get("color"),
            "sizes": data.get("sizes", []),
            "price": float(data.get("price", 0)),
            "stock": int(data.get("stock", 0)),
            "image": data.get("image", "images/placeholder.png"),
            "shoe_type": data.get("shoe_type")
        }
        _PRODUCTS.append(p)
        return p

    def get_all(self) -> List[Dict[str, Any]]:
        return list(_PRODUCTS)

    def get(self, product_id: str) -> Optional[Dict[str, Any]]:
        for p in _PRODUCTS:
            if p["id"] == product_id:
                return p
        return None

    def update_product(self, product_id: str, updates: Dict[str, Any]) -> bool:
        p = self.get(product_id)
        if not p:
            return False

        p.update(updates)
        return True

    def delete_product(self, product_id: str) -> bool:
        global _PRODUCTS
        _PRODUCTS = [p for p in _PRODUCTS if p["id"] != product_id]
        return True

    def search_and_filter(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:



        base = list(_PRODUCTS)


        q = filters.get("q")
        results = self.search_strategy.search(base, q, filters)


        if self.sort_strategy:
            results = self.sort_strategy.sort(results)

        return results

    def reduce_stock(self, product_id: str, qty: int):
        p = self.get(product_id)
        if not p:
            return False, "The product does not exist."
        if p["stock"] < qty:
            return False, "There is not enough stock."
        p["stock"] -= qty
        return True, "OK"
