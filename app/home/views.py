from flask import Response,render_template
from app.home import home



@home.get("/")
def home():
    return render_template("index.html")