import uuid
import hashlib

# Запазваме потребители в памет: list of dicts
_USERS = []

def _hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

class AuthService:
    def __init__(self):
        # Ако още няма потребители, създаваме 1 админ и 2 потребителя (тестови)
        if not _USERS:
            self.register_user("admin@example.com", "admin123", "Admin", "admin")
            self.register_user("user1@example.com", "user123", "User One", "user")
            self.register_user("user2@example.com", "user234", "User Two", "user")

    def register_user(self, email, password, name="User", role="user"):
        if any(u for u in _USERS if u["email"] == email):
            return False, "Email вече съществува."
        user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password_hash": _hash(password),
            "name": name,
            "role": role
        }
        _USERS.append(user)
        # "изпращане" на потвърждение (принтиране в конзолата)
        print(f"[EMAIL SIMULATION] To: {email} | Subject: Welcome | Body: Здравей, {name}! Регистрацията е успешна.")
        return True, "OK"

    def authenticate(self, email, password):
        h = _hash(password)
        for u in _USERS:
            if u["email"] == email and u["password_hash"] == h:
                return True, {"email": u["email"], "name": u["name"], "role": u["role"], "id": u["id"]}
        return False, "Невалидни данни."

    def get_user(self, email):
        for u in _USERS:
            if u["email"] == email:
                return u
        return None
