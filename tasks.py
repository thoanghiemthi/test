from celery import Celery
import uvicorn
from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
import asyncio
conf = ConnectionConfig(
    MAIL_USERNAME='hongnguye617@gmail.com',
    MAIL_PASSWORD='upkasfwqteiywuus',
    MAIL_FROM='hongnguye617@gmail.com',
    MAIL_PORT=587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
app1 = FastAPI()
bodyy = """FastApi send list mail"""
appcelery = Celery('tasks', backend='rpc://', broker='amqp://guest@localhost//')


@appcelery.task
def add(x):
    # pass
    message = MessageSchema(
        subject="Mail_test",
        recipients=x,  # List of recipients, as many as you can pass
        body=bodyy
    )
    fm = FastMail(conf)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fm.send_message(message))


class EmailSchema(BaseModel):
    email: List[EmailStr]


@app1.post("/email")
async def simple_send(
        email: EmailSchema
) -> JSONResponse:
    # print("email.dict()", type(email.dict().get("email"))
    # print("message",message)
    # fm = FastMail(conf)
    add.delay(email.dict().get("email"))
    return JSONResponse(status_code=200, content={"message": "email has been sent"})



if __name__ == "__main__":
    uvicorn.run(app1, host="0.0.0.0", port=8001, log_level="debug")
