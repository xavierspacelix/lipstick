from pydantic import BaseModel, EmailStr


class UpdateProfileRequest(BaseModel):
    name: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class ProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    total_analyses: int


class ProfileStats(BaseModel):
    total_analyses: int
