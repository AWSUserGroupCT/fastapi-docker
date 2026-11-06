from fastapi import FastAPI
from data_models import UserInfo, WorkerResponse
import logging


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logging.info("Application started")
logging.warning("Disk space low")

app = FastAPI()

WORKERS: dict[int, UserInfo] = {
    w.employee_id: w
    for w in [
        UserInfo(employee_id=1, name="Steve", position="Developer", age=22, report_to="John"),
        UserInfo(employee_id=2, name="Jake", position="Developer", age=25, report_to="John"),
        UserInfo(employee_id=3, name="Frank", position="Developer", age=27, report_to="John"),
    ]
}

@app.get("/health")
def get_root():
    return {"message": "healthy"}


@app.post("/api/workers/")
def post_root(user: UserInfo):
    return {"message": user}
    
@app.get("/api/workers/", response_model=WorkerResponse)
def get_worker():
    user = UserInfo(
        employee_id=1,
        name="Steve",
        position="Developer",
        age=22,
        report_to="John",
    )
    return WorkerResponse(message="Worker retrieved successfully", user=user)



@app.get("/api/workers/{worker_id}")
def get_worker_id(worker_id: int):
    worker = WORKERS.get(worker_id)
    logging.info("Worker id: {worker_id}")
    if worker is None:
        raise HTTPException(status_code=404, detail=f"Worker {worker_id} not found")
    return worker
    