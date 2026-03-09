from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "codecourse_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(10))


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    lesson = db.Column(db.Integer)
    completed = db.Column(db.Boolean)


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    due_date = db.Column(db.String(50))


lessons = [
    {"id":1,"title":"What is Python"},
    {"id":2,"title":"Variables"},
    {"id":3,"title":"Loops"},
    {"id":4,"title":"Functions"}
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"],
            role=request.form["role"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":

        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            session["user"] = user.username
            session["role"] = user.role
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=session["user"],
        role=session["role"]
    )


@app.route("/course/python")
def python_course():
    return render_template("course.html", lessons=lessons)


@app.route("/lesson/<int:id>")
def lesson(id):

    lesson = next((l for l in lessons if l["id"] == id), None)

    return render_template("lesson.html", lesson=lesson)


@app.route("/complete/<int:id>")
def complete(id):

    p = Progress(
        user=session["user"],
        lesson=id,
        completed=True
    )

    db.session.add(p)
    db.session.commit()

    return redirect("/course/python")


@app.route("/classroom")
def classroom():

    assignments = Assignment.query.all()

    return render_template(
        "classroom.html",
        assignments=assignments
    )


@app.route("/teacher")
def teacher():

    if session["role"] != "teacher":
        return redirect("/dashboard")

    assignments = Assignment.query.all()

    return render_template(
        "teacher_dashboard.html",
        assignments=assignments
    )


@app.route("/create_assignment", methods=["POST"])
def create_assignment():

    a = Assignment(
        title=request.form["title"],
        due_date=request.form["due"]
    )

    db.session.add(a)
    db.session.commit()

    return redirect("/teacher")


if __name__ == "__main__":
    app.run()
