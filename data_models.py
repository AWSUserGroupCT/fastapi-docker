from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    age: int
    position: str
    report_to: str


class WorkerResponse(BaseModel):
    message: str
    user: UserInfo
