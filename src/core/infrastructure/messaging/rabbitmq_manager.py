# -*- coding: utf-8 -*-
import json

import pika


class RabbitMQManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def send_message(self, queue_name: str, body: json):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port)
            )
            channel = connection.channel()

            try:
                channel.queue_declare(queue=queue_name, passive=True)
            except Exception:
                if channel.is_closed:
                    channel = self.connection.channel()

                channel.queue_declare(
                    queue=queue_name, durable=True, exclusive=False, auto_delete=False
                )

            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            print(f"[x] Sent message to {queue_name}")
        finally:
            connection.close()
