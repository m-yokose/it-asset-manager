from pydantic import BaseModel, EmailStr


class LoginForm(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AccountCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "viewer"  # "admin" | "viewer"


class AccountResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role: str

    model_config = {"from_attributes": True}
