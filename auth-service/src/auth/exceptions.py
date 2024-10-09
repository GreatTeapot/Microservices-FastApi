from fastapi import HTTPException, status


user_already_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User with this email or username already exists",
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

admin_rights_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have enough privileges(super_user)",
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

token_expire = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

cant_validate =HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def validate_user_existence(user):
    if not user:
        raise user_not_found_exception


def validate_user_authentication(user):
    if not user:
        raise credentials_exception
