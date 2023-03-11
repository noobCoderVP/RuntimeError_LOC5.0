from fastapi import APIRouter, Body, Depends
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from server.database import connection
from server.models._utils import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.query import Query
from auth.auth_bearer import JWTBearer


queries = connection("queries")


def query_helper(query) -> dict:
    return {
        "email": query["email"],
        "timing": str(query["timing"]),
        "description": query["description"],
        "images": query["images"],
    }


# Add a new query into to the database
async def add_query(query_data: dict) -> dict:
    try:
        await queries.insert_one(query_data)
        return True
    except:
        return False


async def retrieve_querys():
    q = []
    async for query in queries.find():
        q.append(query_helper(query))
    return q


async def get_queries(email: str):
    q = []
    async for query in queries.find({"email": email}):
        q.append(query_helper(query))
    return q


router = APIRouter()


@router.post(
    "/", response_description="query added", dependencies=[Depends(JWTBearer())]
)
async def addquery(query: Query = Body(...)):
    query = jsonable_encoder(query)
    newquery = await add_query(query)
    if newquery:
        return ResponseModel(True, "Query added successfully!")
    else:
        return ErrorResponseModel("Cannot add query", 403, "Query cannot be added!")


@router.get("/all/")
async def getQueries():
    query = await retrieve_querys()
    if query:
        return ResponseModel(query, "Query data retrieved successfully")
    return ErrorResponseModel("Error", 404, "Query does not exist")


@router.get("/{email}", dependencies=[Depends(JWTBearer())])
async def retrivequery(email: EmailStr):
    query = await get_queries(email)
    if query:
        return ResponseModel(query, "Query data retrieved successfully")
    return ErrorResponseModel("Error", 404, "Query does not exist")
