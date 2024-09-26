from pydantic import BaseModel
from typing import Any, Optional 
import json


class StandardResponse(BaseModel):
    success: bool
    error: Any = None
    body: Any


class BatchData(BaseModel):
    ip: Optional[str] = None
    os: Optional[str] = None
    sdk: Optional[str] = None
    city: Optional[str] = None
    paid: Optional[str] = None
    uuid: Optional[str] = None
    model: Optional[str] = None
    serial: Optional[str] = None
    classId: Optional[int] = None
    country: Optional[str] = None
    product: Optional[str] = None
    version: Optional[str] = None
    courseId: Optional[int] = None
    deviceId: Optional[str] = None
    language: Optional[str] = None
    schoolId: Optional[int] = None
    appVersion: Optional[str] = None
    platformId: Optional[int] = None
    installDate: Optional[str] = None
    manufacturer: Optional[str] = None
    deviceCategory: Optional[int] = None


class User(BaseModel):
    token_id: int
    user_id: int
    honey: Optional[int]

    @classmethod
    def from_query_result(cls, queryResult):
        return cls(
            token_id=queryResult.tokenId,
            user_id=queryResult.userId,
            honey=queryResult.honey
        )

