"""_summary_

Returns:
    _type_: _description_
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from inventory.database.database import get_db
from inventory.jwk_token import verify_token

scopes = {
    "blogs": "Manage Blogs",
    "users": "Manage Users",
    "user:create": "Manage Users.",
}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8003/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """_summary_

    Args:
        security_scopes (SecurityScopes): _description_
        token (str, optional): _description_.
            Defaults to Depends(oauth2_scheme).
        db (Session, optional): _description_.
            Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception, db)
