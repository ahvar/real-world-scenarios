from flask import request, jsonify, render_template


def page_not_found(e):
    if (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    ):
        response = jsonify({"error": "not found"})
        response.status_code = 404
        return response
    render_template("404.html"), 404
