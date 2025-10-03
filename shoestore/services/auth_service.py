import uuid
import hashlib
from typing import List, Dict, Any, Optional, Tuple

_USERS: List[Dict[str, Any]] = []


def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


class AuthService:
    def __init__(self):
        if not _USERS:
            # Seed the same users as before
            self.register_user("admin@example.com", "admin123", "Admin", "admin")
            self.register_user("user1@example.com", "user123", "User One", "user")
            self.register_user("user2@example.com", "user234", "User Two", "user")

    def register_user(self, email: str, password: str, name: str = "User", role: str = "user") -> Tuple[bool, str]:
        if any(u for u in _USERS if u["email"] == email):
            return False, "Email already registered"
        user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password_hash": _hash(password),
            "name": name,
            "role": role
        }
        _USERS.append(user)
        return True, "OK"

    def authenticate(self, email: str, password: str) -> Tuple[bool, Any]:
        h = _hash(password)
        for u in _USERS:
            if u["email"] == email and u["password_hash"] == h:
                return True, {"email": u["email"], "name": u["name"], "role": u["role"], "id": u["id"]}
        return False, "Invalid info."

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        for u in _USERS:
            if u["email"] == email:
                return u
        return None
