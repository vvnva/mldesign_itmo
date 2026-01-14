
from pydantic import BaseModel


class ModelRequest(BaseModel):
    req_id: int | None
    text: str


class ModelResponse(BaseModel):
    req_id: int | None
    card: str
    azs: str
    trk: str
    fuel: str
    topic: str
    sub: str


class ModelRes(BaseModel):
    card: str
    azs: str
    trk: str
    fuel: str
    topic: str
    sub: str
