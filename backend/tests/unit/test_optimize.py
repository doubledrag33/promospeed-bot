from decimal import Decimal
from unittest.mock import MagicMock

from app.models.cart import Cart
from app.services.optimize import generate_plans


def test_generate_plans_handles_empty_cart():
    session = MagicMock()
    cart = Cart()
    cart.items = []
    plans = generate_plans(session, cart, slider=5, user_lat=None, user_lon=None)
    assert len(plans) == 3
    assert all(plan.total == Decimal('0') or plan.total == 0 for plan in plans)
