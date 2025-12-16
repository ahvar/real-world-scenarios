from . import app
from collections import defaultdict
from flask import render_template
import json


def get_all_customers() -> list[tuple]:
    return [
        # id, name, created_at
        (1, "Custom Inks Inc", "2023-01-01"),
        (2, "Hog Heaven Oinc", "2023-02-01"),
        (3, "LL Beam LLC", "2023-03-01"),
        (4, "Weesnaw's Paddywagons", "2024-01-01"),
    ]


def get_all_users() -> list[tuple]:
    return [
        # username, customer_id, active, created_at
        ("dan@custominc.com", 1, True, "2023-01-02"),
        ("john@custominc.com", 1, False, "2023-01-03"),
        ("hog.roger@hoghevvin.com", 2, True, "2023-02-01"),
        ("hog.mike@hoghevvin.com", 2, True, "2023-02-05"),
        ("hog.june@hoghevvin.com", 2, True, "2023-02-21"),
        ("hog.melissa@hoghevvin.com", 2, True, "2023-02-25"),
        ("donald@llbeam.org", 3, False, "2023-03-16"),
        ("jen@llbeam.org", 3, False, "2023-03-17"),
        ("tami@llbeam.org", 3, False, "2023-03-19"),
        ("rufus@weesnawz.gov", 4, True, "2023-01-17"),
        ("stumpy@weesnawz.gov", 4, False, "2023-01-16"),
    ]


@app.route("/")
@app.route("/index")
def index():
    users_by_customer = defaultdict(list)
    for username, customer_id, active, created_at in get_all_users():
        users_by_customer[customer_id].append((username, active, created_at))
    result = []
    for id, name, cust_created_at in get_all_customers():
        active = [name for u, a, ca in users_by_customer[id] if a]
        inactive = [name for u, a, ca in users_by_customer[id] if not a]
        acount = len(active)
        inacount = len(inactive)
        newest_user = (
            max(users_by_customer[id], key=lambda x: x[2])[0]
            if users_by_customer[id]
            else None
        )
        result.append(
            {
                "customer_name": name,  # The name of the customer
                "active_user_count": acount,  # The number of active users
                "inactive_user_count": inacount,  # The number of inactive users
                "active_users": active,  # A list of usernames for active users
                "inactive_users": inactive,  # A list of usernames for inactive users
                "newest_user": newest_user,  # The username of the most recently created user
                "created_at": cust_created_at,  # The date on which the customer entry was created
            }
        )
    return render_template("index.html", result=result)
