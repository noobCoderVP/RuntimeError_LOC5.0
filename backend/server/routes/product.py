from fastapi import APIRouter, Body, Depends
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from server.database import connection
from server.models._utils import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.product import Product, updateProduct
from auth.auth_handler import signJWT

from auth.auth_bearer import JWTBearer

product = connection("product")


def product_helper(product) -> dict:
    return {
        "productid": product["productid"],
        "manufracturer": product["manufracturer"],
        "images": list(product["images"]),
        "sentAt": product["joinedAt"],
        "receivedAt": product["receivedAt"],
        "received": product["received"],
    }


async def retrieve_products(manuid: str):
    products = []
    async for p in product.find({'manufracturer': manuid}):
        products.append(product_helper(p))
    return products


# Add a new product into to the database
async def add_product(product_data: dict) -> dict:
    p = await product.insert_one(product_data)
    if p:
        return True
    else:
        return False


# Retrieve a product with a matching ID
async def retrieve_product(manuid: str, productId: str) -> dict:
    p = await product.find_one({"manufracturer": manuid, 'productId': productId})
    if p:
        return product_helper(p)
    return None


router = APIRouter()


@router.post("/add", response_description="product added")
async def addproduct(p: Product = Body(...)):
    test = await retrieve_product(p.manufracturer, p.productId)
    if test:
        return ErrorResponseModel("Already exist", 403, "product already exists!")
    p = jsonable_encoder(p)
    data = await add_product(p)
    return ResponseModel(data, "Product added successfully!")


@router.get("/{productid}", dependencies=[Depends(JWTBearer())])
async def retriveproduct(productid: str):
    product = await retrieve_product({"productId":productid})
    if product:
        return ResponseModel(product, "Product data retrieved successfully")
    return ErrorResponseModel("Error", 404, "Student does not exist")
