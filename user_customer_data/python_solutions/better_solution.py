# Transform the user and customer data into the format specified output data format.

# **Input Data Formats**

#     Customers
#       - id: int           -- The customer's ID
#       - name: str         -- The customer's name
#       - created_at: str   -- The date on which the customer entry was created, an ISO string

#     Users
#       - username: str      -- The user's username
#       - customer_id: int   -- The ID of the customer to which the user belongs
#       - active: bool       -- Whether or not the user is active
#       - created_at: str    -- The date on which the user entry was created, an ISO string

# **Output Data Format**

# ```
# [
#     {
#         "customer_name": str,        # The name of the customer
#         "active_user_count": int,    # The number of active users
#         "inactive_user_count": int,  # The number of inactive users
#         "active_users": list[str],   # A list of usernames for active users
#         "inactive_users": list[str], # A list of usernames for inactive users
#         "newest_user": str,          # The username of the most recently created user
#         "created_at": str,           # The date on which the customer entry was created
#     }, ...
# ]
# ```


# Your results should be dumped as raw JSON to the console!
from collections import defaultdict
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


users_by_customers = defaultdict(list)
for username, customer_id, active, created_at in get_all_users():
    users_by_customers[customer_id].append((username, active, created_at))

results = []
for id, name, created_at in get_all_customers():
    cust_users = users_by_customers.get(id, [])
    active = [u for u, a, _ in cust_users if a]
    inactive = [u for u, a, _ in cust_users if not a]
    newest_user = [max(cust_users, key=lambda x: x[2])[0] if cust_users else None]
    results.append(
        "customer_name": name, 
        "active_user_count": len(active),
        "inactive_user_count": len(inactive),
        'active_users': active_users,
        'inactive_users': inactive_users,
        "newest_user": newest_user,
        "created_at": created_at
    )
    