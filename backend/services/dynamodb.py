import logging
import os
from typing import Optional

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

CUSTOMERS_TABLE = os.environ.get("CUSTOMERS_TABLE", "customers")
LOYALTY_CARDS_TABLE = os.environ.get("LOYALTY_CARDS_TABLE", "loyalty_cards")
REWARDS_TABLE = os.environ.get("REWARDS_TABLE", "rewards")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_dynamodb = None


def _get_dynamodb():
    global _dynamodb
    if _dynamodb is None:
        _dynamodb = boto3.resource("dynamodb")
    return _dynamodb


def _get_table(table_name: str):
    return _get_dynamodb().Table(table_name)


def _paginated_query(table_name: str, **kwargs) -> list[dict]:
    pass


def _now() -> str:
    pass


def _generate_qr_token() -> str:
    pass


# --------------- Customers ---------------


def create_customer(
    phone_number: str,
    first_name: str,
    email: str,
    birthday: Optional[str],
    marketing_consent: bool,
    outlet_id: str,
) -> dict:
    pass


def get_customer_by_phone(phone_number: str) -> Optional[dict]:
    pass


def get_customer_by_qr_token(qr_token: str) -> Optional[dict]:
    pass


def update_customer(
    phone_number: str,
    first_name: str,
    email: str,
    birthday: Optional[str],
) -> dict:
    pass


# --------------- Loyalty Cards ---------------


def create_loyalty_card(customer_id: str, max_stamps: int = 10) -> dict:
    pass


def get_active_loyalty_card(customer_id: str) -> Optional[dict]:
    pass


def get_all_loyalty_cards(customer_id: str) -> list[dict]:
    pass


def add_stamp_to_card(customer_id: str, card_id: str) -> dict:
    pass


def complete_loyalty_card(customer_id: str, card_id: str) -> dict:
    pass


# --------------- Rewards ---------------


def create_reward(
    customer_id: str,
    card_id: str,
    reward_type: str,
    title: str,
    description: str,
    expires_at: str,
    metadata: Optional[dict] = None,
) -> dict:
    pass


def get_customer_rewards(customer_id: str) -> list[dict]:
    pass


def redeem_reward(
    customer_id: str,
    reward_id: str,
    redemption_channel: Optional[str],
    redemption_outlet_id: Optional[str],
    redemption_staff_id: Optional[str],
) -> dict:
    pass
