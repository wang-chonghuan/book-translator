from fastapi import APIRouter, Body, Depends, status, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from services.authentication import AuthHandler
from models.users import CurrentUser, LoginBase, UserBase


router = APIRouter()
auth_handler = AuthHandler()


@router.post("/register", response_description="Register user")
async def register(request: Request, newUser: UserBase = Body(...)) -> UserBase:
    newUser.password = auth_handler.get_password_hash(newUser.password)
    newUser = jsonable_encoder(newUser)

    existing_email = await request.app.mongodb["users"].find_one(
        {"email": newUser["email"]}
    )
    if existing_email is not None:
        raise HTTPException(
            status_code=409, detail=f"User with email {newUser['email']} already exists"
        )

    existing_username = await request.app.mongodb["users"].find_one(
        {"username": newUser["username"]}
    )
    if existing_username is not None:
        raise HTTPException(
            status_code=409,
            detail=f"User with username {newUser['username']} already exists",
        )

    user = await request.app.mongodb["users"].insert_one(newUser)
    created_user = await request.app.mongodb["users"].find_one(
        {"_id": user.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.post("/login", response_description="Login user")
async def login(request: Request, loginUser: LoginBase = Body(...)) -> str:
    user = await request.app.mongodb["users"].find_one({"email": loginUser.email})

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not auth_handler.verify_password(loginUser.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = auth_handler.encode_token(user["_id"])
    response = JSONResponse(content={"token": token})

    return response


@router.get("/me", response_description="Logged in user data")
async def me(request: Request, userId=Depends(auth_handler.auth_wrapper)):
    currentUser = await request.app.mongodb["users"].find_one({"_id": userId})
    result = CurrentUser(**currentUser).dict()
    result["id"] = userId
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
