from logging import Logger

import grpc

from tests.clients.grpc.logger_interceptor import GRPCLoggerInterceptor
from tests.tools.config.grpc import GRPCClientTestConfig


class GRPCTestClient:
    """
    Базовый gRPC-клиент тестового слоя.

    Его роль — хранить gRPC Channel как инфраструктурную зависимость,
    которая будет переиспользоваться специализированными клиентами сервисов.

    Важно:
    - GRPCTestClient НЕ содержит stub'ов конкретных сервисов;
    - НЕ знает protobuf-контрактов;
    - НЕ реализует доменные методы;
    - НЕ выполняет валидацию и ассерты.

    Он является "контейнером транспорта":
    специализированные клиенты будут принимать channel
    и создавать нужные stubs поверх него.
    """

    def __init__(self, channel: grpc.Channel):
        self.channel = channel


def build_grpc_test_channel(logger: Logger, config: GRPCClientTestConfig) -> grpc.Channel:
    """
    Фабрика создания gRPC Channel для тестового слоя.

    Это единственное место, где:
    - применяется конфигурация gRPC-клиента,
    - создаётся канал,
    - подключаются инфраструктурные interceptors (логирование и далее).

    Почему фабрика важна:
    - все специализированные gRPC-клиенты должны использовать
      единый канал с едиными правилами транспорта;
    - если в будущем потребуется добавить:
        - таймауты по умолчанию,
        - retry policy,
        - прокидывание тестового контекста в metadata,
        - сбор метрик,
      это делается здесь, не изменяя клиентов сервисов.
    """
    channel = grpc.insecure_channel(config.url)
    return grpc.intercept_channel(channel, GRPCLoggerInterceptor(logger=logger))
