from fastapi import FastAPI, status
from .api.main import api_router
from .log import Logger
import sys

log = Logger(logname=__name__,filename='app/base.log').logger


app = FastAPI()
app.include_router(api_router)

