from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

@app.get("/")
def read_root():
    return {"Name": "Sam"}

@app.get("/model_not_valid")
def read_item():
    return {"not_valid_model": True}

@app.get("/malformed_json")
def read_item():
    return f"{'malformed_json': True unquoted_value}"

@app.get("/raise_exception")
def create_item():
    raise NotImplementedError("This endpoint is not yet implemented.")


if __name__ == "__main__":
    run("server_fastapi:app", port=8999, reload=True)