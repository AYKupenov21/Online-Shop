from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, template_folder="../templates", url_prefix="/auth")
auth_service = AuthService()

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name") or email.split("@")[0]
        role = request.form.get("role") or "user"
        ok, msg = auth_service.register_user(email, password, name, role)
        if ok:
            flash("Регистрацията е успешна. Потвърждение изпратено (в конзолата).")
            return redirect(url_for("auth.login"))
        else:
            flash(msg)
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        ok, user_or_msg = auth_service.authenticate(email, password)
        if ok:
            session["user"] = {"email": user_or_msg["email"], "name": user_or_msg["name"], "role": user_or_msg["role"]}
            flash("Успешен вход.")
            return redirect(url_for("catalog.view_catalog"))
        else:
            flash(user_or_msg)
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Излязохте от профила.")
    return redirect(url_for("index"))
