from typing import TypeVar, Generic, Any
from pydantic import BaseModel

DataType = TypeVar("DataType")
T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    message: str | None = ""
    meta: dict | Any | None = {}
    data: T | None = None


class GetListResponseBase(ResponseBase[list[DataType]], Generic[DataType]):
    message: str = "Data got correctly"


class GetResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class PostResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data created correctly"


class PutResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"


class PatchResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data patched correctly"


class DeleteResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"


class TokenResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Token set correctly"


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
