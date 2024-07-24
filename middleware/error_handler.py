from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import FastAPI
from typing import Union
import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

URL : str = os.getenv("URL")

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        
    async def dispatch(self, request: Request, call_next) -> Union[Response, JSONResponse]:
        conn = psycopg2.connect(URL)
        try:
            return await call_next(request)
        except Exception as e:
            conn.rollback()
            return JSONResponse(status_code=500, content={"Error": str(e)})