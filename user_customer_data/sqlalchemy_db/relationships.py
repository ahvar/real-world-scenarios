from sqlalchemy import String
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, declarative_base, Session


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"
    id = mapped_column(primary_key=True)
    customer_name = mapped_column(String(250))
    users = relationship("User", back_populates="customer")
    created_at = Column(String)


class User(Base):
    __tablename__ = "user account"
    id = mapped_column(primary_key=True)
    customer_id = mapped_column(ForeignKey("customer.id"))
    username = mapped_column(String(30))
    customer = relationship("Customer", back_populates="users")
    active = Column(Boolean)


engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    cust = Customer(id=1, name="Custom Inks Inc", created_at="2023-01-01")
