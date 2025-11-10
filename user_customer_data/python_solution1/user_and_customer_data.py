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
import json

output = []
for customer in get_all_customers():
    id, name, created_at = customer
    cust_user_obj = {
        "customer_name": name,
        "active_user_count": 0,
        "inactive_user_count": 0,
        "active_users": [],
        "inactive_users": [],
        "newest_user": "",
        "created_at": created_at,
    }
    most_recent = ""
    for user in get_all_users():
        username, customer_id, active, user_created_at = user
        if customer_id == id:
            if active:
                cust_user_obj["active_user_count"] += 1
                cust_user_obj["active_users"].append(username)
            else:
                cust_user_obj["inactive_user_count"] += 1
                cust_user_obj["inactive_users"].append(username)
            if user_created_at > most_recent:
                cust_user_obj["newest_user"] = username
                most_recent = user_created_at
    output.append(cust_user_obj)

print(json.dumps(output, indent=4))
