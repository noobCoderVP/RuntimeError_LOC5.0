from fastapi import APIRouter, Body, Depends
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from server.database import connection
from server.models._utils import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.manuf import Manuf as Manufr, updateManuf as updateManufr
from auth.auth_handler import signJWT

from auth.auth_bearer import JWTBearer

Manufs = connection("manufracturer")


def Manuf_helper(Manuf) -> dict:
    return {
        "name": Manuf["name"],
        "company": Manuf["company"],
        "email": Manuf['email'],
        "password": Manuf["password"],
        "joinedAt": str(Manuf["joinedAt"]),
        "company": Manuf['company'],
        "ratings": list(Manuf['ratings'])
    }


async def retrieve_Manufs():
    Manufs = []
    async for Manuf in Manufs.find():
        Manufs.append(Manuf_helper(Manuf))
    return Manufs

# check if a user exists
async def check_Manuf(username: str):
    u = await retrieve_Manuf(username)
    if u:
        return u
    return None

# Add a new Manuf into to the database
async def add_Manuf(Manuf_data: dict) -> dict:
    Manuf = await Manufs.insert_one(Manuf_data)
    return signJWT(Manuf_data["username"])


# Retrieve a Manuf with a matching ID
async def retrieve_Manuf(username: str) -> dict:
    Manuf = await Manufs.find_one({"username": username})
    if Manuf:
        return Manuf_helper(Manuf)
    return {}


# Update a Manuf with a matching ID
async def update_Manuf(username: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    Manuf = await Manufs.find_one({"username": username})
    if Manuf:
        updated_Manuf = await Manufs.update_one({"username": username}, {"$set": data})
        if updated_Manuf:
            return True
        return False


router = APIRouter()


@router.post("/register", response_description="Manuf added")
async def addManuf(Manuf: Manufr = Body(...)):
    test = await retrieve_Manuf(Manuf.username)
    if test:
        return ErrorResponseModel("Already exist", 403, "Manuf already exists!")
    Manuf = jsonable_encoder(Manuf)
    token = await add_Manuf(Manuf)
    return ResponseModel(token, "Manufracturer added successfully!")


async def check_Manuf(username: str):
    u = await retrieve_Manuf(username)
    if u:
        return u
    return None


@router.post("/login")
async def Login(Manuf: updateManufr = Body(...)):
    u = check_Manuf(Manuf.username)
    if u:
        test = await retrieve_Manuf(Manuf.username)
        if test["password"] == Manuf.password:
            token = signJWT(Manuf.username)
            return ResponseModel(token, "Logged successfully!")
        else:
            return ErrorResponseModel("Wrong password!", 403, "Check your password")
    else:
        return ErrorResponseModel("Manuf does not exist", 404, "Invalid credentials")


@router.get("/{username}", dependencies=[Depends(JWTBearer())])
async def retriveManuf(username: str):
    Manuf = await retrieve_Manuf(username)
    if Manuf:
        return ResponseModel(Manuf, "Manufracturer data retrieved successfully")
    return ErrorResponseModel("Error", 404, "Manufracturer does not exist")


@router.put("/{username}", dependencies=[Depends(JWTBearer())])
async def updateManuf(username: str, Manuf: updateManufr = Body(...)):
    req = {k: v for k, v in Manuf.dict().items() if v is not None}
    updated_manuf = await update_Manuf(username, req)
    if updated_manuf:
        return ResponseModel(
            "Manuf with username: {} name update is successful".format(username),
            "Manuf updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        403,
        "There was an error updating the student data.",
    )
