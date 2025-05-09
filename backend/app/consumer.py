import aio_pika
import asyncio
import os
from bson.objectid import ObjectId
from app.database import Catalog  # Your MongoDB collection

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")

async def handle_order_completed(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            import json
            payload = json.loads(message.body.decode())
            event_id = payload["event_id"]
            qty = int(payload["quantity"])

            result = Catalog.update_one(
                {"_id": ObjectId(event_id)},
                {"$inc": {"available_tickets": -qty}}
            )

            if result.modified_count:
                print(f"[catalog] Reduced tickets for event {event_id} by {qty}")
            else:
                print(f"[catalog] Failed to update tickets for event {event_id}")

        except Exception as e:
            print(f"[catalog] Error processing message: {e}")

async def consume_events():
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            break
        except:
            print("Waiting for RabbitMQ to be ready...")
            await asyncio.sleep(5)

    channel = await connection.channel()
    exchange = await channel.declare_exchange("order_events", aio_pika.ExchangeType.TOPIC)
    queue = await channel.declare_queue("", exclusive=True)
    await queue.bind(exchange, routing_key="order_completed")

    print("[catalog] Listening for order_completed events...")
    await queue.consume(handle_order_completed)
