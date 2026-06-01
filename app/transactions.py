from sqlalchemy.orm import Session

from app.transaction_models import Transaction


def create_transaction(
    db: Session,
    transaction_id: str,
    store_id: str,
    timestamp: str,
    basket_value: float
):

    txn = Transaction(
        transaction_id=transaction_id,
        store_id=store_id,
        timestamp=timestamp,
        basket_value=basket_value
    )

    db.add(txn)

    db.commit()

    return txn