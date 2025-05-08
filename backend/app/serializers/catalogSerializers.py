def eventEntity(event) -> dict:
    return {
        "id": str(event["_id"]),
        "name": event["name"],
        "description": event["description"],
        "location": event["location"],
        "available_tickets": event["available_tickets"],
        "price": event["price"],
        "image": event["image"],
        "created_at": event["created_at"],
        "updated_at": event["updated_at"]
    }

def orderRequest(order) -> dict:
    return {
        "id": str(order["_id"]),
        "event_id": order["event_id"],
        "event_name": order["event_name"],
        "quantity": order["quantity"],
        "price": order["price"],
        "total_price": order["total_price"],
        "order_time": order["order_time"],
    }