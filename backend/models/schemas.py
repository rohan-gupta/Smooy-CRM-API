from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum


# --------------- Enums ---------------

class CustomerStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    blocked = "blocked"


class LoyaltyCardStatus(str, Enum):
    active = "active"
    completed = "completed"
    expired = "expired"


class RewardType(str, Enum):
    welcome_20_percent = "welcome_20_percent"
    fifth_stamp_treat = "fifth_stamp_treat"
    tenth_stamp_reward = "tenth_stamp_reward"
    birthday_reward = "birthday_reward"


class RewardStatus(str, Enum):
    available = "available"
    redeemed = "redeemed"
    expired = "expired"


# --------------- Customers ---------------

class CreateCustomerRequest(BaseModel):
    phoneNumber: str = Field(..., min_length=1)
    firstName: str
    email: EmailStr
    birthday: str
    marketingConsent: bool = False
    outletId: str = Field(default="pasir_ris_mall")


class UpdateCustomerRequest(BaseModel):
    firstName: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[str] = None
    marketingConsent: Optional[bool] = None
    status: Optional[CustomerStatus] = None
    outletId: Optional[str] = None


class CustomerResponse(BaseModel):
    customerId: str
    phoneNumber: str
    firstName: str
    email: str
    birthday: Optional[str] = None
    memberQrToken: Optional[str] = None


# --------------- Loyalty Cards ---------------

class CreateLoyaltyCardRequest(BaseModel):
    customerId: str = Field(..., min_length=1)
    outletId: str = Field(default="pasir_ris_mall")
    maxStamps: int = Field(default=10, gt=0)


class UpdateLoyaltyCardRequest(BaseModel):
    cardId: str
    customerId: str
    currentStampCount: int = Field(default=None, ge=0)
    status: Optional[LoyaltyCardStatus] = None


class LoyaltyCardResponse(BaseModel):
    cardId: str
    customerId: str
    maxStamps: int
    currentStampCount: int
    status: LoyaltyCardStatus
    startedAt: str
    completedAt: Optional[str] = None
    expiresAt: str
    createdAt: str
    updatedAt: str


# --------------- Rewards ---------------

class RewardMetadata(BaseModel):
    discountPercent: Optional[int] = None
    rewardValue: Optional[float] = None
    rewardUnit: Optional[str] = None


class CreateRewardRequest(BaseModel):
    customerId: str = Field(..., min_length=1)
    cardId: Optional[str] = None
    rewardType: RewardType
    title: str = Field(..., min_length=1)
    description: str = ""
    expiresAt: str = Field(..., min_length=1)
    metadata: Optional[RewardMetadata] = None


class UpdateRewardRequest(BaseModel):
    status: Optional[RewardStatus] = None
    redemptionChannel: Optional[str] = None
    redemptionOutletId: Optional[str] = None
    redemptionStaffId: Optional[str] = None


class RewardResponse(BaseModel):
    rewardId: str
    customerId: str
    cardId: Optional[str] = None
    rewardType: RewardType
    title: str
    description: str
    status: RewardStatus
    unlockedAt: str
    redeemedAt: Optional[str] = None
    expiresAt: str
    redemptionChannel: Optional[str] = None
    redemptionOutletId: Optional[str] = None
    redemptionStaffId: Optional[str] = None
    metadata: Optional[RewardMetadata] = None
    createdAt: str
    updatedAt: str


# --------------- Generic ---------------

class MessageResponse(BaseModel):
    message: str
