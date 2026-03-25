from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from botocore.exceptions import ClientError

from models.schemas import (
    CreateCustomerRequest,
    CustomerResponse,
    MessageResponse,
    UpdateLoyaltyCardRequest,
    RewardResponse,
)

from services.dynamodb import (
    create_customer,
    get_customer,
    get_loyalty_card_details,
    add_loyalty_card_stamp,
    list_rewards,
)

app = FastAPI(title="Smooy Loyalty API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/customers", response_model=MessageResponse, status_code=201)
def create_customer_endpoint(body: CreateCustomerRequest):
    try:
        create_customer(body.phoneNumber, body.firstName, body.email, body.birthday)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=400, detail=f"User already exists: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    return {"message": f"User {body.phoneNumber} created successfully"}


@app.get("/customers/{phone}", response_model=CustomerResponse)
def get_customer_endpoint(phone: str):
    user = get_customer(phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "customerId": user["customerId"],
        "phoneNumber": user["phoneNumber"],
        "firstName": user["firstName"],
        "email": user["email"],
        "birthday": user["birthday"],
    }



@app.get("/loyalty/{customer_id}", response_model=MessageResponse, status_code=200)
def get_loyalty_card_details_endpoint(customer_id: str):
    loyalty_card_details = get_loyalty_card_details(customer_id)
    return {
        "cardId": loyalty_card_details["cardId"],
        "customerId": loyalty_card_details["customerId"],
        "maxStamps": loyalty_card_details["maxStamps"],
        "currentStampCount": loyalty_card_details["currentStampCount"],
        "status": loyalty_card_details["status"],
        "startedAt": loyalty_card_details["startedAt"],
        "completedAt": loyalty_card_details["completedAt"],
    }


@app.post("/loyalty/stamp", response_model=MessageResponse, status_code=200)
def add_loyalty_card_stamp_endpoint(body: UpdateLoyaltyCardRequest):
    try:
        add_loyalty_card_stamp(body.customerId, body.cardId, body.currentStampCount)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=400, detail=f"Loyalty card not found: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    return {"message": f"Loyalty card stamp added successfully"}


@app.get("/rewards/{customer_id}", response_model=list[RewardResponse], status_code=200)
def list_rewards_endpoint(customer_id: str):
    items = list_rewards(customer_id)
    return [
        {
            "reward_id": r["reward_id"],
            "name": r["name"],
            "description": r["description"],
            "points_required": int(r["points_required"]),
            "created_at": r["created_at"],
        }
        for r in items
    ]


handler = Mangum(app)
