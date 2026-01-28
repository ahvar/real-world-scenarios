from . import app


@app.route("/v1/plans?state=<state>&rate_area=<rate_area>&metal_level=<metal_level")
def get_plans(state, rate_area, metal_level):
    """
    Get the available plans and rates by state, rate area, and metal level

    :param state: Description
    :param rate_area: Description
    :param metal_level: Description
    :return plans: plan IDs and rates
    """
    pass


@app.route("/v1/plans?state=<state>")
def get_plans(state):
    """
    Get available plans by state

    :param state: Description
    :return plans: plan IDs, metal levels, and rates
    """
    pass


@app.route("/v1/rate_area?state=<state>&zipcode=<zipcode>")
def get_rate_area(state, zipcode):
    pass


@app.route("/v1/rate_areas?zipcode=<zipcode>")
def get_rate_areas(zipcode):
    pass
