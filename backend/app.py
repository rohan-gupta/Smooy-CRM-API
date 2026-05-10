from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from models.schemas import (
    CreateCustomerRequest,
    CustomerResponse,
    LoyaltyCardResponse,
    MessageResponse,
    AddStampRequest,
    RedeemRewardRequest,
    RewardResponse,
)
from services.dynamodb import (
    create_customer,
    create_loyalty_card,
    get_customer_by_phone,
    get_customer_by_qr_token,
    get_all_loyalty_cards,
    add_stamp_to_card,
    get_customer_rewards,
    redeem_reward,
)

app = FastAPI(title="Smooy Loyalty API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------- Customers ---------------

@app.post("/customers", response_model=MessageResponse, status_code=201)
def create_customer_endpoint(body: CreateCustomerRequest):
    pass


@app.get("/customers/{phone_number}", response_model=CustomerResponse)
def get_customer_by_phone_endpoint(phone_number: str):
    pass


@app.get("/customers/qr/{qr_token}", response_model=CustomerResponse)
def get_customer_by_qr_endpoint(qr_token: str):
    pass


# --------------- Loyalty Cards ---------------

@app.get("/loyalty/{customer_id}", response_model=list[LoyaltyCardResponse])
def get_loyalty_cards_endpoint(customer_id: str):
    pass


@app.post("/loyalty/{customer_id}/stamp", response_model=MessageResponse)
def add_stamp_endpoint(customer_id: str, body: AddStampRequest):
    pass


# --------------- Rewards ---------------

@app.get("/rewards/{customer_id}", response_model=list[RewardResponse])
def get_rewards_endpoint(customer_id: str):
    pass


@app.post("/rewards/{customer_id}/{reward_id}/redeem", response_model=MessageResponse)
def redeem_reward_endpoint(customer_id: str, reward_id: str, body: RedeemRewardRequest):
    pass


# --------------- Auth (stub — requires OTP/Cognito integration) ---------------

@app.post("/auth/otp/send", response_model=MessageResponse)
def send_otp_endpoint():
    pass


@app.post("/auth/otp/verify", response_model=MessageResponse)
def verify_otp_endpoint():
    pass


@app.post("/auth/staff/login", response_model=MessageResponse)
def staff_login_endpoint():
    pass


handler = Mangum(app)
