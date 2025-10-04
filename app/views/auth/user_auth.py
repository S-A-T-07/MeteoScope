from datetime import datetime

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
            user = supabase_client.auth.sign_up(
                {"email": email, "password": password})
            if user.user:
                # Insert into user table using user_id (uuid)
                supabase_client.table("user").insert(
                    {
                        "user_id": user.user.id,  # ✅ Correct column
                        "name": name,
                    }
                ).execute()
                # print(f"user_id : {user.user.id}")

            return redirect(url_for("auth.prefer"))
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
            # ✅ Redirect to prefer after login
            return redirect(url_for("user.dashboard"))
        except Exception as e:
            return f"Login failed: {e}"

    return render_template("login.html")


@auth_bp.route("/prefer", methods=["GET", "POST"])
def prefer():
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

    return render_template("prefer.html", message=message)


# Logout route
@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


# Create_Event route


@auth_bp.route("/create_event", methods=["GET", "POST"])
def create_event():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        event_name = request.form["event_name"]
        user_id = session["user"]["id"]

        try:
            profile = supabase_client.table("user").select(
                "name").eq("user_id", user_id).execute()
            user_name = profile.data[0]["name"] if profile.data else "Unknown"

            supabase_client.table("event").insert({
                "user_id": user_id,
                "event_name": event_name
            }).execute()

            return "✅ Event created successfully! <a href='/auth/create_event'>Create another</a>"
        except Exception as e:
            return f"❌ Error creating event: {e}"

    return render_template("create_event.html")

# Create Team


@auth_bp.route("/create_team", methods=["GET", "POST"])
def create_team():
    if "user" not in session:
        return redirect(url_for("auth_bp.login"))

    # Fetch all users for dropdown
    users = supabase_client.table("user").select("user_id,name").execute().data

    if request.method == "POST":
        team_name = request.form["team_name"]
        selected_user_ids = request.form.getlist(
            "user_ids")  # returns a list of UUID strings

        # Fetch names for selected UUIDs
        selected_users = [u["user_id"]
                          for u in users if u["user_id"] in selected_user_ids]
        print(f"id : {selected_users}")

        ids = ""
        for id in selected_users:
            ids = f"{ids},{id}"
        # print(f"{ids=}")

        try:
            supabase_client.table("team").insert({
                "team_name": team_name,
                "user_id": session["user"]["id"],       # ✅ Pass as Python list
                "user_ids": ids
            }).execute()
            return render_template("create_team.html", users=users, message="✅ Team created successfully!")
        except Exception as e:
            return render_template("create_team.html", users=users, message=f"❌ Error creating team: {e}")

    return render_template("create_team.html", users=users)
