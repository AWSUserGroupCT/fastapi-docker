from fastapi import FastAPI
from data_models import UserInfo, WorkerResponse


app = FastAPI()

@app.get("/health")
def get_root():
    return {"message": "healthy"}


@app.post("/api/workers/")
def post_root(user: UserInfo):
    return {"message": user}
    
@app.get("/api/workers/", response_model=WorkerResponse)
def get_worker():
    user = UserInfo(
        name="Steve",
        position="Developer",
        age=22,
        report_to="John",
    )
    return {"message": { "user": user }}
