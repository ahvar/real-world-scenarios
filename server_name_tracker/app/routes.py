from app import app
from flask import render_template


@app.route("/", methods=["GET"])
@app.route("index", methods=["GET"])
def index():
    return render_template("index.html", messages=[])


@app.route("/allocate/<hosttype>", methods=["POST"])
def allocate(hosttype):
    pass


@app.route("/deallocate/<hostname>", methods=["POST"])
def deallocate(hostname):
    pass


@app.route("/allocations")
def allocations():
    pass
