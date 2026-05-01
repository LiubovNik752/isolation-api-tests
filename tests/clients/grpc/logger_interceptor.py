from logging import Logger

from grpc import UnaryUnaryClientInterceptor


class GRPCLoggerInterceptor(UnaryUnaryClientInterceptor):
    """
    Инфраструктурный interceptor gRPC-клиента тестового слоя.

    Задача interceptor'а — фиксировать факт gRPC-взаимодействия
    на уровне транспорта, а не на уровне бизнес-логики.

    Почему это важно в контексте тестов:
    - при падении интеграционного теста лог gRPC-вызовов — первое,
      что позволяет понять, "куда мы сходили" и "на каком вызове упали";
    - логирование должно быть централизованным и одинаковым
      для всех gRPC-клиентов, а не реализованным вручную в каждом методе;
    - interceptor — это стандартный механизм gRPC для таких задач.

    Границы ответственности:
    interceptor НЕ знает:
    - какой тест выполняется,
    - какой сервис вызывается (он видит только имя метода),
    - какие доменные данные передаются,
    - какие схемы ответов ожидаются.

    Он знает только одно:
    "выполнен gRPC-вызов метода <method>".
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    def intercept_unary_unary(self, continuation, client_call_details, request):
        self.logger.info(f"REQUEST: {client_call_details.method}")
        response = continuation(client_call_details, request)
        self.logger.info(f"RESPONSE: {client_call_details.method}")

        return response
