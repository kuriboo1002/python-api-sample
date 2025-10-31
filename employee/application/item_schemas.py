from pydantic import BaseModel
from typing import Optional

class ItemCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

    from pydantic import field_validator

    @field_validator("name")
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("nameは必須です")
        return v

    @field_validator("description")
    def description_max_length(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 255:
            raise ValueError("descriptionは255文字以内で入力してください")
        return v

class ItemUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None

    from pydantic import field_validator

    @field_validator("name")
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("nameは必須です")
        return v

    @field_validator("description")
    def description_max_length(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 255:
            raise ValueError("descriptionは255文字以内で入力してください")
        return v

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
