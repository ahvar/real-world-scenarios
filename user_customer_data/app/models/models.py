from .. import db
from datetime import date
from sqlalchemy import String, Date, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Customer(db.Model):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    created_date: Mapped[date] = mapped_column(Date, default=date.today)
    users = relationship("User", back_populates="customer")


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64))
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), index=True, nullable=False
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    customer = relationship("Customer", back_populates="users")
