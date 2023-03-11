from fastapi import APIRouter, Body, Depends
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from server.database import connection
from server.models._utils import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.retailer import Retailer, updateRetailer
from auth.auth_handler import signJWT

from auth.auth_bearer import JWTBearer

retailer = connection("retailer")


def Retail_helper(Retail) -> dict:
    return {
        "username": Retail["username"],
        "company": Retail["company"],
        "email": Retail['email'],
        "password": Retail["password"],
        "joinedAt": str(Retail["joinedAt"]),
        "orders": list(Retail['orders'])
    }


async def retrieve_retailers():
    retailer = []
    async for Retail in retailer.find():
        retailer.append(Retail_helper(Retail))
    return retailer

# check if a user exists
async def check_retailer(username: str):
    u = await retrieve_retailer(username)
    if u:
        return u
    return None

# Add a new Retail into to the database
async def add_retailer(Retail_data: dict) -> dict:
    Retail = await retailer.insert_one(Retail_data)
    return signJWT(Retail_data["username"])


# Retrieve a Retail with a matching ID
async def retrieve_retailer(username: str) -> dict:
    Retail = await retailer.find_one({"username": username})
    if Retail:
        return Retail_helper(Retail)
    return {}


# Update a Retail with a matching ID
async def update_retailer(username: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    Retail = await retailer.find_one({"username": username})
    if Retail:
        Retail = await retailer.update_one({"username": username}, {"$set": data})
        if Retail:
            return True
        return False


router = APIRouter()


@router.post("/register", response_description="Retail added")
async def Register(Retail: Retailer = Body(...)):
    test = await check_retailer(Retail.username)
    if test:
        return ErrorResponseModel("Already exist", 403, "Retail already exists!")
    Retail = jsonable_encoder(Retail)
    token = await add_retailer(Retail)
    return ResponseModel(token, "Retailracturer added successfully!")

@router.post("/login")
async def Login(Retail: updateRetailer = Body(...)):
    u = check_retailer(Retail.username)
    if u:
        test = await retrieve_retailer(Retail.username)
        if test["password"] == Retail.password:
            token = signJWT(Retail.username)
            return ResponseModel(token, "Logged successfully!")
        else:
            return ErrorResponseModel("Wrong password!", 403, "Check your password")
    else:
        return ErrorResponseModel("Retail does not exist", 404, "Invalid credentials")


@router.get("/{username}", dependencies=[Depends(JWTBearer())])
async def Details(username: str):
    Retail = await retrieve_retailer(username)
    if Retail:
        return ResponseModel(Retail, "Retailracturer data retrieved successfully")
    return ErrorResponseModel("Error", 403, "Retailracturer does not exist")


@router.put("/{username}", dependencies=[Depends(JWTBearer())])
async def Retail(username: str, Retail: Retailer = Body(...)):
    req = {k: v for k, v in Retail.dict().items() if v is not None}
    check = await check_retailer(username)
    if check:
        test = await update_retailer(username, Retail)
        if test:
            return ResponseModel(
            "Retail with username: {} name update is successful".format(username),
            "Retail updated successfully",
        )
        else:
            ErrorResponseModel("server database error", 503, "error updating the database")  
    return ErrorResponseModel(
        "An error occurred",
        403,
        "There was an error updating the student data.",
    )
