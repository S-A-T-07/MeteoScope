from flask import Blueprint, redirect, render_template, request, session, url_for

from app.supabase.supabase_client import supabase_client

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("/create_event", methods=["GET", "POST"])
def create_event():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        event_name = request.form["event_name"]
        user_id = session["user"]["id"]

        try:
            profile = (
                supabase_client.table("user")
                .select("name")
                .eq("user_id", user_id)
                .execute()
            )
            user_name = profile.data[0]["name"] if profile.data else "Unknown"

            supabase_client.table("event").insert(
                {"user_id": user_id, "event_name": event_name}
            ).execute()

            return "✅ Event created successfully! <a href='/auth/create_event'>Create another</a>"
        except Exception as e:
            return f"❌ Error creating event: {e}"

    return render_template("create_event.html")


# Create Team


@tasks_bp.route("/create_team", methods=["GET", "POST"])
def create_team():
    if "user" not in session:
        return redirect(url_for("auth_bp.login"))

    # Fetch all users for dropdown
    users = supabase_client.table("user").select("user_id,name").execute().data

    if request.method == "POST":
        team_name = request.form["team_name"]
        selected_user_ids = request.form.getlist(
            "user_ids"
        )  # returns a list of UUID strings

        # Fetch names for selected UUIDs
        selected_users = [
            u["user_id"] for u in users if u["user_id"] in selected_user_ids
        ]
        print(f"id : {selected_users}")

        ids = ""
        for id in selected_users:
            ids = f"{ids},{id}"
        # print(f"{ids=}")

        try:
            supabase_client.table("team").insert(
                {
                    "team_name": team_name,
                    "user_id": session["user"]["id"],  # ✅ Pass as Python list
                    "user_ids": ids,
                }
            ).execute()
            return render_template(
                "create_team.html", users=users, message="✅ Team created successfully!"
            )
        except Exception as e:
            return render_template(
                "create_team.html", users=users, message=f"❌ Error creating team: {e}"
            )

    return render_template("create_team.html", users=users)
