import redis
import datetime
import os

from http.client import HTTPException
from fastapi import APIRouter
from pydantic import BaseModel


# 1. Создаём роутер для антифрода
router = APIRouter(
    prefix="/antifraud",
    tags=["antifraud"],
)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    decode_responses=True
)

try:
    redis_client.ping()
    print("Redis подключен")
except:
    print("Redis не доступен")
    redis_client = None

# классы с конфигами данных

class Loan(BaseModel):
    amount: int
    loan_data: str
    is_closed: bool

class CheckRequest(BaseModel):
    birth_date: str
    phone_number: str
    loans_history: list[Loan]


def calculate_data(birth_date: str) -> int:
    try:
        birth = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(
            400,
            f'Неверный формат: {birth_date}'
        )

    today = datetime.date.today()
    age = today.year - birth.year
    if today.month < birth.month:
        age -= 1

    return age

# 2. Создаём endpoint /antifraud/check
@router.post("/check")
async def check_client(request: CheckRequest):
    """
    Проверка клиента на антифрод правила.

    """
    stop_factors = []
    passed = True

    if redis_client:
        blacklisted = redis_client.sismember('blacklist:phones', request.phone_number)
        if blacklisted:
            stop_factors.append(f'Телефон {request.phone_number} в чёрном списке')
            passed = False

    age = calculate_data(request.birth_date)
    if age < 18:
        stop_factors.append(f'Недопустимый возраст: {age}')
        passed = False

    if not (request.phone_number.startswith('+7') or request.phone_number.startswith('8')):
        stop_factors.append(f'Неверный формат номера: {request.phone_number}')
        passed = False

    for loan in request.loans_history:
        if not loan.is_closed:
            stop_factors.append(f"Есть открытый кредит на сумму {loan.amount}")
            passed = False

    return {
        "message": "Антифрод система работает!",
        "stop_factors": stop_factors,
        "passed": passed
    }


@router.post("/admin/blacklist/add")
async def add_to_blacklist(phone: str, reason: str = ""):
    if not redis_client:
        raise HTTPException(503,
                            "Redis не доступен")

    redis_client.sadd("blacklist:phones", phone)
    if reason:
        redis_client.set(f"reason:{phone}", reason)

    return {
        "status": "ok",
        "message": f"Телефон {phone} добавлен в чёрный список"
    }


@router.delete("/admin/blacklist/remove/{phone}")
async def remove_from_blacklist(phone: str):
    if not redis_client:
        raise HTTPException(503,
                            "Redis не доступен")

    redis_client.srem("blacklist:phones", phone)
    redis_client.delete(f"reason:{phone}")

    return {
        "status": "ok",
        "message": f"Телефон {phone} удалён из чёрного списка"
    }
#   docker run -p 8080:8001 service-template:latest


