from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Float

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(
        String,
        primary_key=True
    )

    store_id = Column(
        String,
        index=True
    )

    timestamp = Column(
        String
    )

    basket_value = Column(
        Float
    )