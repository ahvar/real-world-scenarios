from . import bp


@bp.route("/", methods=["GET", "POST"])
def index():
    pass
