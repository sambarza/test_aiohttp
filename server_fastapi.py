from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from uvicorn import run

app = FastAPI()

@app.get("/")
def read_root():
    return {"MyName": "Sam"}

@app.get("/model_not_valid")
def read_item():
    return {"not_valid_model": True}

@app.get("/malformed_json", response_class=PlainTextResponse)
def read_item():
    return f"Ciao"

@app.get("/raise_exception")
def create_item():
    raise NotImplementedError("This endpoint is not yet implemented.")


if __name__ == "__main__":
    run("server_fastapi:app", port=8999, reload=True)