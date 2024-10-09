# news_service/rpc_client.py
import uuid

import aio_pika
import asyncio


async def request_author_validation(author_id: int) -> bool:
    connection = await aio_pika.connect("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()

    # Declare a queue to send the request
    request_queue = await channel.declare_queue("auth_queue")

    # Create a unique queue for replies
    callback_queue = await channel.declare_queue(exclusive=True)

    # Create a correlation ID to match requests with replies
    correlation_id = str(uuid.uuid4())

    # Send the request message to the 'auth_queue'
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=str(author_id).encode(),
            reply_to=callback_queue.name,
            correlation_id=correlation_id
        ),
        routing_key="auth_queue"
    )

    # Wait for the response
    response_message = await callback_queue.get()
    return response_message.body.decode() == 'true'
