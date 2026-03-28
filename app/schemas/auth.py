from pydantic import BaseModel, ConfigDict, EmailStr


class RoleRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    role: RoleRead

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

