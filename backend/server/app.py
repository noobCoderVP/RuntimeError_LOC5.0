from fastapi import FastAPI

from server.routes.user import router as userRouter
from server.routes.manuf import router as manufRouter
from server.routes.retailer import router as retailRouter
from server.routes.query import router as queryRouter
from server.routes.transaction import router as transRouter
from server.routes.product import router as productRouter

app = FastAPI()

app.include_router(userRouter, tags=["Users"], prefix="/user")
app.include_router(manufRouter, tags=["Manufracturer"], prefix="/manuf")
app.include_router(retailRouter, tags=["Retailer"], prefix="/retail")
app.include_router(queryRouter, tags=["Queries"], prefix="/query")
app.include_router(transRouter, tags=["Transactions"], prefix="/transactions")
app.include_router(productRouter, tags=["Products"], prefix="/products")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
