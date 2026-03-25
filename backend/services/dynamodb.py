import os
import hashlib
from datetime import datetime, timezone
from typing import Optional

import boto3
from boto3.dynamodb.conditions import Key


CUSTOMERS_TABLE = os.environ.get("CUSTOMERS_TABLE", "customers")
LOYALTY_TABLE = os.environ.get("LOYALTY_TABLE", "loyalty")
REWARDS_TABLE = os.environ.get("REWARDS_TABLE", "rewards")
LOYALTY_CARDS_TABLE = os.environ.get("LOYALTY_CARDS_TABLE", "loyalty_cards")


dynamodb = boto3.resource("dynamodb")
customers_table = dynamodb.Table(CUSTOMERS_TABLE)
loyalty_table = dynamodb.Table(LOYALTY_TABLE)
rewards_table = dynamodb.Table(REWARDS_TABLE)
loyalty_cards_table = dynamodb.Table(LOYALTY_CARDS_TABLE)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# --------------- Users ---------------


def create_customer(phone: str, firstName: str, email: str, birthday: Optional[str] = None) -> dict:
    now = _now()
    print(f"Creating customer {phone} with name {firstName} and email {email} and birthday {birthday}")
    customer_id = hashlib.md5((phone + email).encode()).hexdigest()
    item = {
        "PK": f"USER#{phone}",
        "SK": f"CUSTOMER#{customer_id}",
        "customerId": customer_id,
        "phoneNumber": phone,
        "firstName": firstName,
        "email": email,
        "birthday": birthday,
        "created_at": now,
    }
    customers_table.put_item(
        Item=item,
        ConditionExpression="attribute_not_exists(PK) AND attribute_not_exists(SK)",
    )
    return item


def get_customer(phone: str) -> Optional[dict]:
    resp = customers_table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{phone}") & Key("SK").begins_with("CUSTOMER#"),
        Limit=1,
    )
    items = resp.get("Items", [])
    return items[0] if items else None


# --------------- Loyalty Cards ---------------


def get_loyalty_card_details(customer_id: str) -> Optional[dict]:
    resp = loyalty_cards_table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{customer_id}") & Key("SK").begins_with("LOYALTY_CARD#")
    )
    items = resp.get("Items", [])
    return items[0] if items else None


def add_loyalty_card_stamp(customer_id: str, card_id: str, current_stamp_count: int) -> dict:
    now = _now()
    item = {
        "PK": f"USER#{customer_id}",
        "SK": f"LOYALTY_CARD#{card_id}",
        "cardId": card_id,
        "currentStampCount": current_stamp_count,
    }
    loyalty_cards_table.put_item(Item=item)
    return item


# --------------- Rewards ---------------

def list_rewards(customer_id: str) -> list[dict]:
    resp = rewards_table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{customer_id}") & Key("SK").begins_with("REWARD#")
    )
    return resp.get("Items", [])


def redeem_loyalty_reward(customer_id: str, reward_id: str) -> dict:
    now = _now()
    item = {
        "PK": f"USER#{customer_id}",
        "SK": f"REWARD#{reward_id}",
        "rewardId": reward_id,
    }
    rewards_table.put_item(Item=item)
    return item
