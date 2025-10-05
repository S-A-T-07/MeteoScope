from flask import Blueprint, redirect, render_template, request, session, url_for

from app.supabase.supabase_client import supabase_client

event_bp = Blueprint("event", __name__, url_prefix="/user")


@event_bp.route("/create_event", methods=["GET", "POST"])
def create_event():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        event_name = request.form["event_name"]
        event_date = request.form["event_date"]
        event_location = request.form["event_location"]
        event_select = request.form["event_select"]
        user_id = session["user"]["id"]

        data = {
            "event_name": event_name,
            "event_date": event_date,
            "event_location": event_location,
            "event_select": event_select,
            "user_id": user_id,
        }

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
