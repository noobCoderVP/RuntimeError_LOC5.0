from fastapi import FastAPI

from server.routes.user import router as userRouter

app = FastAPI()

app.include_router(userRouter, tags=["Users"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
