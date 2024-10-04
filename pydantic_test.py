from pydantic import BaseModel, EmailStr, validator, field_validator


class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int

    @field_validator('account_id')
    def validate_account_id(cls, value):
        if value <= 0:
            raise ValueError(f'account_id {value} must be positive')
        return value

user1 = User(
    name="rog",
    email="rog@dp.com",
    account_id=23,
)

print(f"user1 is {user1}")

user2_data = {
    'name': 'iang',
    'email': 'ig@dp.com',
    'account_id': 19
}

user2 = User(**user2_data)
print(f"user2 is {user2}")
