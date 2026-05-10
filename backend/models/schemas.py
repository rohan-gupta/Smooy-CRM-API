from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum


# --------------- Enums ---------------

class LoyaltyCardStatus(str, Enum):
    active = "active"
    completed = "completed"
    expired = "expired"


class RewardType(str, Enum):
    welcome_discount = "welcome_discount"
    stamp_treat = "stamp_treat"
    birthday_reward = "birthday_reward"


class RewardStatus(str, Enum):
    available = "available"
    redeemed = "redeemed"
    expired = "expired"


# --------------- Customers ---------------

class CreateCustomerRequest(BaseModel):
    phone_number: str = Field(..., min_length=1)
    first_name: str = Field(..., min_length=1)
    email: EmailStr
    birthday: Optional[str] = None
    marketing_consent: bool = False
    outlet_id: str = Field(default="pasir_ris_mall")


class CustomerResponse(BaseModel):
    customer_id: str
    phone_number: str
    first_name: str
    email: str
    birthday: Optional[str] = None
    marketing_consent: bool = False
    outlet_id: str
    member_qr_token: str


# --------------- Loyalty Cards ---------------

class AddStampRequest(BaseModel):
    card_id: str = Field(..., min_length=1)


class LoyaltyCardResponse(BaseModel):
    card_id: str
    customer_id: str
    max_stamps: int
    current_stamp_count: int
    status: LoyaltyCardStatus
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: str
    updated_at: str


# --------------- Rewards ---------------

class RewardMetadata(BaseModel):
    discount_percent: Optional[int] = None
    reward_value: Optional[float] = None
    reward_unit: Optional[str] = None


class RedeemRewardRequest(BaseModel):
    redemption_channel: Optional[str] = None
    redemption_outlet_id: Optional[str] = None
    redemption_staff_id: Optional[str] = None


class RewardResponse(BaseModel):
    reward_id: str
    customer_id: str
    card_id: Optional[str] = None
    reward_type: str
    title: str
    description: str
    status: RewardStatus
    unlocked_at: str
    redeemed_at: Optional[str] = None
    expires_at: Optional[str] = None
    redemption_channel: Optional[str] = None
    redemption_outlet_id: Optional[str] = None
    redemption_staff_id: Optional[str] = None
    metadata: Optional[RewardMetadata] = None
    created_at: str
    updated_at: str


# --------------- Generic ---------------

class MessageResponse(BaseModel):
    message: str
