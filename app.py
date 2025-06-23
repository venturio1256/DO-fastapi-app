from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to venturio Labs/v1/test "}