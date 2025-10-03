from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class SearchStrategy(ABC):
    @abstractmethod
    def search(self, products: List[Dict[str, Any]], q: Optional[str], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class LinearSearch(SearchStrategy):

    def search(self, products: List[Dict[str, Any]], q: Optional[str], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = products


        if q:
            q_lower = q.lower()
            results = [
                p for p in results
                if q_lower in (p.get("name") or "").lower() or q_lower in (p.get("description") or "").lower()
            ]


        color = filters.get("color")
        if color:
            c = color.lower()
            results = [p for p in results if c in ((p.get("color") or "").lower())]


        shoe_type = filters.get("shoe_type")
        if shoe_type:
            st = shoe_type.lower()
            results = [p for p in results if (p.get("shoe_type") or "").lower() == st]


        size = filters.get("size")
        if size:
            results = [p for p in results if size in [str(s) for s in (p.get("sizes") or [])]]


        min_price = filters.get("min_price")
        if min_price is not None:
            results = [p for p in results if float(p.get("price") or 0) >= min_price]

        max_price = filters.get("max_price")
        if max_price is not None:
            results = [p for p in results if float(p.get("price") or 0) <= max_price]


        if filters.get("in_stock"):
            results = [p for p in results if p.get("stock", 0) > 0]

        return results
