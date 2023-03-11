from fastapi import APIRouter, Body, Depends
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from server.database import connection
from server.models._utils import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.user import User, updateUser
from auth.auth_handler import signJWT

from auth.auth_bearer import JWTBearer

users = connection("users")


def user_helper(user) -> dict:
    return {
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        "joinedAt": str(user["joinedAt"]),
        "profession": user["profession"],
        "gender": user["gender"],
    }


async def retrieve_users():
    users = []
    async for user in users.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await users.insert_one(user_data)
    return signJWT(user_data["email"])


# Retrieve a user with a matching ID
async def retrieve_user(email: str) -> dict:
    user = await users.find_one({"email": email})
    if user:
        return user_helper(user)
    return {}


# Update a user with a matching ID
async def update_user(email: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await users.find_one({"email": email})
    if user:
        updated_user = await users.update_one({"email": email}, {"$set": data})
        if updated_user:
            return True
        return False


router = APIRouter()


@router.post("/register", response_description="User added")
async def addUser(user: User = Body(...)):
    test = await retrieve_user(user.email)
    if test:
        return ErrorResponseModel("Already exist", 403, "User already exists!")
    user = jsonable_encoder(user)
    token = await add_user(user)
    return ResponseModel(token, "Student added successfully!")


async def check_user(email: str):
    u = await retrieve_user(email)
    if u:
        return u
    return None


@router.post("/login")
async def Login(user: updateUser = Body(...)):
    u = check_user(user.email)
    if u:
        test = await retrieve_user(user.email)
        if test["password"] == user.password:
            token = signJWT(user.email)
            return ResponseModel(token, "Logged successfully!")
        else:
            return ErrorResponseModel("Wrong password!", 403, "Check your password")
    else:
        return ErrorResponseModel("User does not exist", 404, "Invalid credentials")


@router.get("/{email}", dependencies=[Depends(JWTBearer())])
async def retriveUser(email: EmailStr):
    user = await retrieve_user(email)
    if user:
        return ResponseModel(user, "Student data retrieved successfully")
    return ErrorResponseModel("Error", 404, "Student does not exist")


@router.put("/{email}", dependencies=[Depends(JWTBearer())])
async def updateUser(email: EmailStr, user: updateUser = Body(...)):
    req = {k: v for k, v in user.dict().items() if v is not None}
    updated_student = await update_user(email, req)
    if updated_student:
        return ResponseModel(
            "User with email: {} name update is successful".format(email),
            "User updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )
