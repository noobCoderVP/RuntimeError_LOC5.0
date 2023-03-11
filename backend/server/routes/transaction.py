from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from server.database import connection
from server.models._utils import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.transaction import Transaction
from auth.auth_handler import signJWT

from auth.auth_bearer import JWTBearer

transaction = connection("transaction")


def Trans_helper(trans) -> dict:
    return {
        "doneby": trans["doneby"],
        "productId": trans["productId"],
        "transactorid": trans['transactorid'],
        "executedAt": trans["executedAt"],
    }


async def retrieve_transactions(transactorid):
    transactions = []
    async for Trans in transaction.find({'transactorid': transactorid}):
        transactions.append(Trans_helper(Trans))
    return transactions

# check if a user exists
async def check_transaction(productId: str, transid: str):
    u = await transaction.find_one({"productId": productId, "transactorid": transid})
    if u:
        return True
    return False

# Add a new Trans into to the database
async def add_transaction(Trans_data: dict) -> None:
    Trans = await transaction.insert_one(Trans_data)
    return Trans

router = APIRouter()


@router.post("/execute",dependencies=[Depends(JWTBearer())], response_description="Trans added")
async def Execute(Trans: Transaction = Body(...)):
    test = await check_transaction(Trans.transactorid, Trans.productId)
    if test:
        return ErrorResponseModel("Transaction has been done!", 403, "Trans already exists!")
    Trans = jsonable_encoder(Trans)
    token = await add_transaction(Trans)
    return ResponseModel(token, "Transaction added successfully!")

@router.get("/{transactorid}", dependencies=[Depends(JWTBearer())])
async def Details(transactorid: str):
    Trans = await retrieve_transactions(transactorid)
    if Trans:
        return ResponseModel(Trans, "Transracturer data retrieved successfully")
    return ErrorResponseModel("Error", 403, "Transracturer does not exist")

