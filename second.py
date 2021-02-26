from flask import Blueprint, render_template

second = Blueprint("second",__name__, static_folder="static",template_folder="templates")

@app1.route('/')
def home():
    return "Homepage. Method used %s" %request.method

app1.run()