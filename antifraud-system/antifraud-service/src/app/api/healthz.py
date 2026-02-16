from fastapi import APIRouter, Response, status



router = APIRouter(
    prefix="/healthz",
    tags=["system"],
)

@router.get("/live")
async def liveness_probe() -> Response:
    """
    healthz.py - блок для проверки:
        отвечает ли он на запросы
        знать, на какой сервер отправлять трафик
        для Docker/Kubernetes (системы проверяют, готов ли контейнер)
        для мониторинга (автоматические системы следят за этим endpoint)
    """

    """
    Простая проверка на то, что приложение запущено и работает.
    """
    return Response(status_code=status.HTTP_200_OK)

