from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "codecourse_secret"

lessons = [
    {"id":1,"title":"What is Python?"},
    {"id":2,"title":"Variables"},
    {"id":3,"title":"Print Statements"},
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

@app.route("/course/python")
def python_course():
    return render_template("course_python.html", lessons=lessons)

@app.route("/lesson/<int:id>")
def lesson(id):
    lesson = next((l for l in lessons if l["id"] == id), None)
    return render_template("lesson.html", lesson=lesson)

@app.route("/classroom")
def classroom():
    return render_template("classroom.html")

if __name__ == "__main__":
    app.run()
