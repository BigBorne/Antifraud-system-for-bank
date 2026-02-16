import logging

from fastapi import FastAPI
from app.api import healthz
from app.antifraud import check


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

app = FastAPI(title='Anti Fraud')


app.include_router(check.router)
app.include_router(healthz.router)
