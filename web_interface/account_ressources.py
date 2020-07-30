from pydantic import validate_arguments, BaseModel


class AccountResources(BaseModel):
    account_id: str

