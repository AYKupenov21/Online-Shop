from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


class QuickSortByPrice(SortStrategy):

    def sort(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        items = list(products)

        def _price_key(p):
            try:
                return float(p.get("price") or 0)
            except Exception:
                return 0.0

        def quicksort(arr):
            if len(arr) <= 1:
                return arr
            pivot = _price_key(arr[len(arr) // 2])
            left = [x for x in arr if _price_key(x) < pivot]
            middle = [x for x in arr if _price_key(x) == pivot]
            right = [x for x in arr if _price_key(x) > pivot]
            return quicksort(left) + middle + quicksort(right)

        return quicksort(items)
