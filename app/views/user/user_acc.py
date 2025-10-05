from flask import Blueprint, redirect, render_template, session, url_for, request
from app.supabase.supabase_client import supabase_client
user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html", user=session["user"])


@user_bp.route("/prefer", methods=["GET", "POST"])
def prefer():
    if "user" not in session:
        return redirect(url_for("login"))

    message = None
    if request.method == "POST":
        very_hot = request.form.get("very_hot")
        very_cold = request.form.get("very_cold")
        very_windy = request.form.get("very_windy")
        very_wet = request.form.get("very_wet")

        try:
            # Insert values into Supabase table
            supabase_client.table("user").update({
                "very_hot": very_hot,
                "very_cold": very_cold,
                "very_windy": very_windy,
                "very_wet": very_wet,
            }).eq("user_id", session["user"]["id"]).execute()
            message = "✅ Values saved successfully!"
        except Exception as e:
            message = f"❌ Error saving values: {e}"

    return render_template("prefer.html", message=message)
