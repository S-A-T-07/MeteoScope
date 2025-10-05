from flask import Blueprint, redirect, render_template, request, session, url_for

from app.supabase.supabase_client import supabase_client

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


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

            return redirect(url_for("user.prefer"))
        except Exception as e:
            return f"❌ Error creating account: {e}"

    return render_template("signup.html")


# Login route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error_message = None  # initialize here
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = supabase_client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if user.user is None:
                # Invalid credentials
                error_message = "Login failed: Invalid login credentials"
            else:
                session["user"] = user.user.dict()  # Store user session
                return redirect(url_for("user.dashboard"))
        except Exception as e:
            error_message = f"Login failed: {e}"

    return render_template("login.html", error_message=error_message)


# Logout route
@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))
