from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService
import re

auth_bp = Blueprint("auth", __name__, template_folder="../templates", url_prefix="/auth")
auth_service = AuthService()

# Helper function for password strength
def is_strong_password(password: str) -> bool:
    """Password must be at least 8 chars, contain uppercase, lowercase, digit, and special char."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        name = request.form.get("name", "").strip() or email.split("@")[0]
        role = request.form.get("role", "user").strip()

        # --- Validation rules ---
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.")
            return render_template("register.html")

        if not is_strong_password(password):
            flash("Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character.")
            return render_template("register.html")

        if len(name) < 2:
            flash("Name must be at least 2 characters long.")
            return render_template("register.html")

        if role not in ["user", "admin"]:
            flash("Invalid role.")
            return render_template("register.html")

        ok, msg = auth_service.register_user(email, password, name, role)
        if ok:
            flash("The registration was successful.")
            return redirect(url_for("auth.login"))
        else:
            flash(msg)

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Both email and password are required.")
            return render_template("login.html")

        ok, user_or_msg = auth_service.authenticate(email, password)
        if ok:
            session["user"] = {
                "email": user_or_msg["email"],
                "name": user_or_msg["name"],
                "role": user_or_msg["role"],
            }
            flash("Successfully logged in.")
            return redirect(url_for("catalog.view_catalog"))
        else:
            flash(user_or_msg)

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.")
    return redirect(url_for("index"))
