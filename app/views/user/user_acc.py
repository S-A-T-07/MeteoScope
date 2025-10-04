from flask import Blueprint, redirect, render_template, session, url_for

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html", user=session["user"])
