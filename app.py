from flask import Flask, render_template, request, redirect, session
from models import db, User, Photo   

      import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.secret_key = "change_this_secret"
db.init_app(app)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user and user.password == request.form['password']:
            session["user"] = user.username
            session["role"] = user.role
            return redirect('/dashboard')

        return "Login greșit"

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect('/login')

    if session["role"] == "admin":
        return redirect('/admin')

    photos = Photo.query.filter_by(student=session["user"]).all()
    return render_template("album.html", photos=photos)


@app.route('/admin', methods=['GET','POST'])
def admin():
    if session.get("role") != "admin":
        return "Acces interzis"

    if request.method == 'POST':
        url = request.form['url']
        student = request.form['student']

        photo = Photo(url=url, student=student)
        db.session.add(photo)
        db.session.commit()

    return render_template("admin.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
