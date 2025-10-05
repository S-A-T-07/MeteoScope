from flask import Blueprint, redirect, render_template, request, session, url_for

from app.supabase.supabase_client import supabase_client

event_bp = Blueprint("event", __name__, url_prefix="/user")


@event_bp.route("/events", methods=["GET", "POST"])
def list_events():
    if "user" not in session:
        return redirect(url_for("login"))

    user_id = session["user"]["id"]

    # Fetch events created by the logged-in user
    events = (
        supabase_client.table("event")
        .select("id, event_name, event_date, event_location, team_id")
        .eq("user_id", user_id)
        .execute()
        .data
    )

    # Fetch team names for each event
    for event in events:
        team = (
            supabase_client.table("team")
            .select("team_name")
            .eq("id", event["team_id"])
            .execute()
            .data
        )
        event["team_name"] = team[0]["team_name"] if team else "Unknown"

    return render_template("events/list_events.html", events=events)


@event_bp.route("/create_event", methods=["GET", "POST"])
def create_event():
    if "user" not in session:
        return redirect(url_for("login"))

    # Fetch all teams for dropdown
    teams = supabase_client.table("team").select("id, team_name").execute().data

    if request.method == "POST":
        event_name = request.form["event_name"]
        event_date = request.form["event_date"]
        event_location = request.form["event_location"]
        team_id = request.form["team_select"]  # team selected from dropdown
        user_id = session["user"]["id"]

        try:
            # Fetch the logged-in user's name
            profile = (
                supabase_client.table("user")
                .select("name")
                .eq("user_id", user_id)
                .execute()
            )
            user_name = profile.data[0]["name"] if profile.data else "Unknown"

            # Insert the event into Supabase
            supabase_client.table("event").insert(
                {
                    "event_name": event_name,
                    "event_date": event_date,
                    "event_location": event_location,
                    "team_id": team_id,
                    "user_id": user_id,
                }
            ).execute()

            return render_template(
                "events/create_event.html",
                teams=teams,
                message="✅ Event created successfully!",
            )
        except Exception as e:
            return render_template(
                "events/create_event.html",
                teams=teams,
                message=f"❌ Error creating event: {e}",
            )

    return render_template(
        "events/create_event.html", teams=teams, user_id=session["user"]["id"]
    )
