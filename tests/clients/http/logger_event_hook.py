from logging import Logger

from httpx import Request, Response


class HTTPLoggerEventHook:
    """
    Инфраструктурный обработчик событий HTTP-клиента.

    Используется для логирования запросов и ответов
    на уровне транспортного слоя.

    Этот класс не знает:
    - какой тест выполняется,
    - какой сервис вызывается,
    - какие данные передаются.

    Его задача — зафиксировать факт HTTP-взаимодействия
    в логах тестового окружения.
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    def request(self, request: Request):
        self.logger.info(
            f"{request.method} {request.url} - Waiting for response"
        )

    def response(self, response: Response): 
        request = response.request
        self.logger.info(
            f"{request.method} {request.url} - Status {response.status_code}"
        )
