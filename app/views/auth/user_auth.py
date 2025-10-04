from datetime import datetime

from flask import Blueprint, redirect, render_template, request, session, url_for

from app.supabase.supabase_client import supabase_client

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            # Create user in Supabase Auth
            user = supabase_client.auth.sign_up({"email": email, "password": password})
            if user.user:
                # Insert into user table using user_id (uuid)
                supabase_client.table("user").insert(
                    {
                        "user_id": user.user.id,  # ✅ Correct column
                        "name": name,
                    }
                ).execute()
                # print(f"user_id : {user.user.id}")

            return "✅ Account created! <a href='/login'>Login here</a>"
        except Exception as e:
            return f"❌ Error creating account: {e}"

    return render_template("signup.html")


# Login route


# Login route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = supabase_client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            session["user"] = user.user.dict()  # Store user session
            # ✅ Redirect to dashboard after login
            return redirect(url_for("dashboard"))
        except Exception as e:
            return f"Login failed: {e}"

    return render_template("login.html")


# Dashboard route


@auth_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth_bp.login"))

    message = None
    if request.method == "POST":
        very_hot = request.form.get("very_hot")
        very_cold = request.form.get("very_cold")
        very_windy = request.form.get("very_windy")
        very_wet = request.form.get("very_wet")

        try:
            # Insert values into Supabase table
            supabase_client.table("user").update(
                {
                    "very_hot": very_hot,
                    "very_cold": very_cold,
                    "very_windy": very_windy,
                    "very_wet": very_wet,
                    "created_at": datetime.utcnow().isoformat(),
                }
            ).eq("user_id", session["user"]["id"]).execute()
            message = "✅ Values saved successfully!"
        except Exception as e:
            message = f"❌ Error saving values: {e}"

    return render_template("dashboard.html", message=message)


# Logout route
@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))
