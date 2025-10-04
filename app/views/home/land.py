from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    # if "user" in session:
    #     # Fetch profile from Supabase
    #     profile = (
    #         supabase.table("user")
    #         .select("name")
    #         .eq("user_id", session["user"]["id"])
    #         .execute()
    #     )
    #     name = profile.data[0]["name"] if profile.data else "User"
    #     return f"✅ Welcome {name} ({session['user']['email']}) <br><a href='/logout'>Logout</a>"
    # return (
    #     "Not logged in <br><a href='/login'>Login</a> | <a href='/signup'>Sign Up</a>"
    # )

    return render_template("home/land.html")
