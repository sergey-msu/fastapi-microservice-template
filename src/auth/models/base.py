'''
    Application base model
'''
from pydantic import BaseModel
from pydantic import ConfigDict


class AppBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
