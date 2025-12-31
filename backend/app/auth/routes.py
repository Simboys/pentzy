from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Password = Admin@123
USERS = {
    "admin": {
        "password": "$pbkdf2-sha256$29000$pZRybq3VGgNgbE2J0dobYw$ZzXJeZDRMOJMXbC2ona9ZzsYcGvQ.YhJt6VkJsajv0s",
        "role": "admin"
    }
}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": form_data.username, "role": user["role"]}
    )
    return {"access_token": token, "token_type": "bearer"}
