# # auth_service/rpc_server.py
#
# import asyncio
# from aio_pika import connect, IncomingMessage
#
# async def handle_request(message: IncomingMessage):
#     author_id = int(message.body.decode())
#
#     # Here, you would fetch the author from the database
#     # Assuming you have a User model to check the author
#     author_exists = check_author_exists(author_id)  # Define this function
#
#     response = 'true' if author_exists else 'false'
#
#     # Send the response back to the client
#     await message.reply(response.encode())
#
#
# async def main():
#     # Connect to RabbitMQ
#     connection = await connect("amqp://guest:guest@rabbitmq/")
#     channel = await connection.channel()
#
#     # Declare a queue for requests
#     queue = await channel.declare_queue("auth_queue")
#
#     # Start listening for messages
#     await queue.consume(handle_request)
#
#     print(" [x] Awaiting RPC requests")
#     await asyncio.Future()
#
#
# def check_author_exists(author_id: int) -> bool:
#     # This would be a database query
#     # Example: return db_session.query(User).filter_by(id=author_id).first() is not None
#     return True  # Mock for simplicity
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
