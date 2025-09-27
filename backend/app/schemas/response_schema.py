from typing import TypeVar, Generic, Any
from pydantic import BaseModel

DataType = TypeVar("DataType")
T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    message: str = ""
    meta: dict | Any | None = {}
    data: T | None = None


class GetListResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data got correctly"
    data: list[DataType]


class GetResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data got correctly"


class PostResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data created correctly"


class PutResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data updated correctly"


class PatchResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data patched correctly"


class DeleteResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data deleted correctly"


class TokenResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str | None = "Token set correctly"


def create_response(
    data: DataType, message: str | None = None, meta: dict | Any | None = {}
) -> (
    GetResponseBase[DataType]
    | PostResponseBase[DataType]
    | PutResponseBase[DataType]
    | DeleteResponseBase[DataType]
    | GetListResponseBase[DataType]
    | TokenResponseBase[DataType]
):
    if message is None:
        return {"data": data, "meta": meta}
    return {"data": data, "msg": message, "meta": meta}
