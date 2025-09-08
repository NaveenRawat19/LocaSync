from fastapi import FastAPI, HTTPException, Depends, status
from common_lib.db import mongodb_client
from user_service.app.models import UserCreate, UserInDB, UserOut
from user_service.app.auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="User Service")
user_collection = mongodb_client.get_collection("users")

@app.post("/signup", response_model=UserOut)
async def signup(user: UserCreate):
    try:
        existing_user = user_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = hash_password(user.password)
        user_dict = user.dict()
        user_dict["hashed_password"] = hashed_pw
        del user_dict["password"]

        result = user_collection.insert_one(user_dict)
        user_out = UserOut(id=str(result.inserted_id), email=user.email, username=user.username)
        return {"status": "success", "message": "User Added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    user = user_collection.find_one({"email": form_data.username})
    print(user)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
