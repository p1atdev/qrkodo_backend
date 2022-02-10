from fastapi import FastAPI
from api.routers import qrcode

app = FastAPI()
app.include_router(qrcode.router)


@app.get("/hello")
async def hello():
    return {"message": "hello world!"}
