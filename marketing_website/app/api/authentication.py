from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


def verify_password(email, password):
    if email == "":
        return False
