from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order

router = APIRouter()


@router.patch("/orders/{order_id}/address")
def update_order_address(
    order_id: int,
    new_address: str,
    customer_id: int,
    db: Session = Depends(get_db),
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    db.query(Order).filter(
        Order.customer_id == customer_id
    ).update({
        "shipping_address": new_address
    })

    db.commit()

    return {
        "order_id": order_id,
        "shipping_address": new_address,
    }