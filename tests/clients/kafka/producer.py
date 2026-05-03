import logging

import allure
from confluent_kafka import Producer

from tests.tools.config.kafka import KafkaClientTestConfig


class KafkaProducerTestClient:
    """
    Kafka producer тестового слоя.

    Этот клиент отвечает исключительно за публикацию сообщений
    в Kafka-топики в рамках тестов.

    Важная архитектурная позиция курса:
    - тест инициирует бизнес-флоу через событие;
    - обработка события и бизнес-логика происходят
      на стороне сервисов (consumer'ов);
    - тестовый код не читает Kafka и не содержит consumer'ов.

    Таким образом, KafkaProducerTestClient — это
    инфраструктурный инструмент запуска event-driven сценариев,
    а не часть бизнес-логики тестов.
    """

    def __init__(
        self,
        config: KafkaClientTestConfig,
        logger: logging.Logger,
    ):
        self.logger = logger

        self.producer = Producer({"bootstrap.servers": config.bootstrap_servers,})

    @allure.step("Produce message to topic {topic}")
    def produce(self, topic: str, value: str | bytes):
        """
        Публикация одного сообщения в Kafka-топик.

        Бизнес-смысл метода:
        - тест публикует событие;
        - сервис-processor читает его как consumer;
        - далее запускается асинхронный бизнес-флоу.

        Клиент не знает:
        - структуру события;
        - бизнес-смысл payload;
        - кто именно и когда обработает сообщение.
        """
        try:
            self.producer.produce(topic, value)
            self.producer.poll(0)

            self.logger.info(f"Kafka message produced {topic}")
        except Exception as error:
            self.logger.exception(f"Kafka produce failed {topic}:{error}")
            raise

    @allure.step("Flush all messages")
    def flush_all(self, timeout: float = 10.0):
        """
        Принудительное ожидание отправки всех сообщений.

        Этот метод используется в тестах, где важно гарантировать,
        что все события были доставлены в Kafka
        до выполнения последующих шагов (например, чтения через API).

        flush — это синхронизационная точка между
        асинхронным миром Kafka и детерминированным тестом.
        """
        self.logger.info("Kafka producer flush started")
        self.producer.flush(timeout=timeout)
        self.logger.info("Kafka producer flush finished")
