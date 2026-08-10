from datetime import datetime, timedelta
from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



SECRET_KEY = "real-time-leaderboard-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bearer_scheme = HTTPBearer()

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})   
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        username: str = payload.get("sub")
        if username is None:
            return None

        return username
    except jwt.JWTError:
        return None

def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    username = verify_access_token(token.credentials)
    print(username)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return username
