from pydantic import BaseModel, EmailStr, field_validator, Field,ConfigDict


class LoginRequest(BaseModel):
    donor_id : int
    password:str = Field(...,min_length=5,max_length=20)

class RegisterRequest(BaseModel):
   name: str
   email: EmailStr
   mobile: str = Field(...,min_length=10,max_length=15)
   monthly_amount = int
   address: str =Field(...,min_length=5, max_length=80)
   password: str = Field(...,min_length=6,max_length=20)

@field_validator("name")
@classmethod
def validate_name(cls,value):
    value =value.strip()
    if not value:
        raise ValueError("Name Can't be Empty")
    return value

@field_validator("mobile")
@classmethod
def validate_mobile(cls,value):
    value =value.strip()
    if not value.isdigit():
        raise ValueError("Mobile Must contain only Digits")
    if len(value) != 10:
        raise ValueError("Mobile number must be exactly 10  Digits")
    return value
@field_validator("password")
@classmethod
def validate_password(cls,value):
    value =value.strip()
    if not (c.isupper() for c in value):
        raise ValueError("password must contain uppercase letter")
    if not (c.islower() for c in value):
            raise ValueError("password must contain lowercase letter")
    if not (c.isdigit() for c in value):
            raise ValueError("password must contain a number")
    return value



#Responses 
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr | None
    mobile: str
    address: str | None
    is_active:bool
    is_verified:bool

    model_config = ConfigDict(
        from_attributes=True
    )


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
    donor: UserResponse

class MessageResponse(BaseModel):
     message: str
     model_config = ConfigDict(
            from_attributes=True
    ) 

         
class RegisterResponse(BaseModel):
     message: str
     donor_id:int


class MeResponse(BaseModel):
     message: str
     donor: UserResponse