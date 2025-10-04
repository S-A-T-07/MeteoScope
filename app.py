
from flask import Flask, request, session, redirect, url_for, render_template
from supabase_client import supabase
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key"   # Needed for Flask sessions

# Home route


@app.route("/")
def index():
    if "user" in session:
        # Fetch profile from Supabase
        profile = supabase.table("user").select("name").eq(
            "user_id", session["user"]["id"]).execute()
        name = profile.data[0]["name"] if profile.data else "User"
        return f"✅ Welcome {name} ({session['user']['email']}) <br><a href='/logout'>Logout</a>"
    return "Not logged in <br><a href='/login'>Login</a> | <a href='/signup'>Sign Up</a>"

# Signup route


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            # Create user in Supabase Auth
            user = supabase.auth.sign_up(
                {"email": email, "password": password})
            if user.user:
                # Insert into user table using user_id (uuid)
                supabase.table("user").insert({
                    "user_id": user.user.id,  # ✅ Correct column
                    "name": name
                }).execute()
                # print(f"user_id : {user.user.id}")

            return "✅ Account created! <a href='/login'>Login here</a>"
        except Exception as e:
            return f"❌ Error creating account: {e}"

    return render_template("signup.html")

# Login route


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = supabase.auth.sign_in_with_password(
                {"email": email, "password": password})
            session["user"] = user.user.dict()  # Store user session
            # ✅ Redirect to dashboard after login
            return redirect(url_for("dashboard"))
        except Exception as e:
            return f"Login failed: {e}"

    return render_template("login.html")

# Dashboard route


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
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
            supabase.table("user").update({
                "very_hot": very_hot,
                "very_cold": very_cold,
                "very_windy": very_windy,
                "very_wet": very_wet,
                "created_at": datetime.utcnow().isoformat()
            }).eq("user_id", session["user"]["id"]).execute()
            message = "✅ Values saved successfully!"
        except Exception as e:
            message = f"❌ Error saving values: {e}"

    return render_template("dashboard.html", message=message)

# Logout route


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
