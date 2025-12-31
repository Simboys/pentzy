from fastapi import Depends, HTTPException
from app.auth.deps import get_current_user

def require_role(required_roles: list):
    def role_checker(user: dict = Depends(get_current_user)):
        user_role = user.get("role")
        if user_role not in required_roles:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
        return user
    return role_checker
