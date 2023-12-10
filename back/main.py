from typing import Union

from fastapi import FastAPI
from uvicorn import run

from config import Config, setup_logging
from periodic_tasks import init_scheduler

app = FastAPI()




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.on_event("startup")
def startup_event():
    init_scheduler(config=config)


if __name__ == '__main__':
    setup_logging()
    config = Config()
    run(app, host="0.0.0.0", port=5000)
