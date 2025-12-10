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
import json
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    users = relationship("User", back_populates="customer")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    active = Column(Boolean, nullable=False)
    created_at = Column(String, nullable=False)
    customer = relationship("Customer", back_populates="users")


def setup_database():
    engine = create_engine("sqlite://:memory:", echo=False)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session


def populate_database(session):
    for customer_data in get_all_customers():
        id, name, created_at = customer_data
        customer = Customer(id=id, name=name, created_at=created_at)
        session.add(customer)

    users_data = get_all_users()


output = []
for customer in get_all_customers():
    id, name, created_at = customer
    user_obj = {
        "name": name,
        "created_at": created_at,
        "active_user_count": 0,
        "inactive_user_count": 0,
        "active_users": [],
        "inactive_users": [],
        "newest_user": "",
    }
    newest = ""
    for user in get_all_users():
        username, customer_id, active, user_created_at = user
        if id == customer_id:
            if active:
                user_obj["active_user_count"] += 1
                user_obj["active_users"].append(username)
            else:
                user_obj["inactive_user_count"] += 1
                user_obj["inactive_users"].append(username)
            if user_created_at > newest:
                user_obj["created_at"] = username
    output.append(user_obj)
print(json.dumps(output, indent=4))
