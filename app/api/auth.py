from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.config import Config

security = HTTPBearer()

def authenticate(credentials: HTTPAuthorizationCredentials = Security(security)):
    """验证Bearer令牌"""
    if credentials.credentials != Config.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
