from datetime import datetime, timedelta
import os

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

from db import mycursor
from logic import books as books_logic, reviews as reviews_logic, users as users_logic, user_books as user_books_logic


def create_app():
    """Factory to create and configure the Flask app."""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")

    # ---------------------------------------------------------------------
    # Helper queries
    # ---------------------------------------------------------------------
    def get_top_books_of_week():
        """Return top 3 books finished this week ordered by average rating."""
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        sql = """
            SELECT b.id, b.title, b.authors, b.average_rating
            FROM user_books ub
            JOIN books b ON ub.book_id = b.id
            WHERE ub.end_date >= %s
            GROUP BY b.id
            ORDER BY b.average_rating DESC
            LIMIT 3
        """
        try:
            mycursor.execute(sql, (one_week_ago,))
            result = mycursor.fetchall()
        except Exception as e:
            print(f"Error fetching top books: {e}")
            result = []
        mycursor.clear_attributes()
        return result

    def get_user_books_for_profile(user_id):
        """Return current reading book (first with status 'reading') and list of recently read books (status 'read' ordered by end_date desc)."""
        raw_list = user_books_logic.get_user_list(user_id) or []
        reading = []
        read = []
        want = []
        for row in raw_list:
            title, status, start_date, end_date = row
            if status == "reading":
                reading.append({"title": title, "status": status})
            elif status == "read":
                read.append({"title": title, "status": status})
            elif status == "want to read":
                want.append({"title": title, "status": status})
        return reading, read, want

    # ---------------------------------------------------------------------
    # Routes
    # ---------------------------------------------------------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/blog")
    def blog():
        # Most recent reviews
        recent_reviews = reviews_logic.get_recent_reviews()
        top_books = get_top_books_of_week()
        return render_template("blog.html", reviews=recent_reviews, top_books=top_books)

    # Simple JSON search endpoint used by the JS search bar
    @app.route("/api/search")
    def api_search():
        query = request.args.get("q", "")
        if not query:
            return jsonify([])
        results = books_logic.search_by_title(query)
        return jsonify(results)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user_id = users_logic.login(username, password)
            if user_id:
                session["user_id"] = user_id
                session["username"] = username
                flash("Login successful!", "success")
                return redirect(url_for("profile"))
            else:
                flash("Incorrect username or password.", "error")
                return redirect(url_for("login"))
        return render_template("signin.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            if users_logic.signup(username, password):
                flash("Registered successfully! Please sign in.", "success")
                return redirect(url_for("login"))
            else:
                flash("Username is already taken.", "error")
                return redirect(url_for("register"))
        return render_template("register.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out.", "success")
        return redirect(url_for("index"))

    @app.route("/profile")
    def profile():
        if "user_id" not in session:
            return redirect(url_for("login"))
        user_id = session["user_id"]
        reading_books, recent_books, want_books = get_user_books_for_profile(user_id)

        display_books = []
        # add all reading books first
        for rb in reading_books:
            if len(display_books) >= 5:
                break
            display_books.append({"title": rb["title"], "current": True, "status": "reading"})

        # fill remaining with recent (read) books
        for b in recent_books:
            if len(display_books) >= 5:
                break
            display_books.append({"title": b["title"], "current": False, "status": "read"})

        # pad to 5 with None
        while len(display_books) < 5:
            display_books.append(None)

        # build my list display
        mylist_display = []
        for w in want_books:
            if len(mylist_display) >= 5:
                break
            mylist_display.append({"title": w["title"], "current": False, "status": "want"})
        while len(mylist_display) < 5:
            mylist_display.append(None)

        return render_template(
            "profile.html",
            username=session.get("username"),
            recent_books=display_books,
            my_list=mylist_display,
        )

    @app.route("/api/start-reading", methods=["POST"])
    def api_start_reading():
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json()
        if not data or "title" not in data:
            return jsonify({"error": "Missing title"}), 400
        success = user_books_logic.update_book_status(session["user_id"], data["title"], "reading")
        return jsonify({"success": success})

    # ------------------------------------------------------------------
    return app


if __name__ == "__main__":
    create_app().run(debug=True) 