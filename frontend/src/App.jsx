import React, { useEffect, useState } from 'react';
import "./styles.css";

function EventList() {
  const [events, setEvents] = useState([]);
  const [quantities, setQuantities] = useState({}); // Track quantities per event
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8004/api/catalog/events")
      .then((res) => res.json())
      .then((data) => {
        const qtyMap = {};
        data.forEach(event => {
          qtyMap[event.id] = 1;
        });
        setQuantities(qtyMap);
        setEvents(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch events", err);
        setLoading(false);
      });
  }, []);

  const updateQty = (id, delta) => {
    setQuantities(prev => ({
      ...prev,
      [id]: Math.max(1, (prev[id] || 1) + delta)
    }));
  };

  const handleBuy = (event) => {
    console.log("event passed to handleBuy:", event);
    const quantity = quantities[event.id];
    const payload = {
      event_id: String(event.id),
      event_name: event.name,
      quantity,
      price: event.price,
      total_price: event.price * quantity,
      order_time: new Date().toISOString()
    };
  
    fetch("http://localhost:8002/api/orders", {
      method: "POST",
      credentials: 'include',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    })
      .then(async res => {
        if (!res.ok) {
          const errorText = await res.text();
          throw new Error(errorText || "Unknown error");
        }
  
        const contentType = res.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
          const data = await res.json();
          alert("Order placed successfully!");
          console.log(data);
        } else {
          alert("Order placed, but response format is unexpected.");
        }
      })
      .catch(err => {
        console.error("Order failed", err);
        alert("Order failed!");
      });
  };
  

  if (loading) return <p>Loading events...</p>;

  return (
    <div className="event-container">
      {events.map((event) => {
        const imageSrc = event.image.startsWith("http")
          ? event.image
          : `http://localhost:8000${event.image}`;

        return (
          <div key={event.id} className="event-card">
            <div className="image-container">
              <img src={imageSrc} alt={event.name} className="photo" />
            </div>
            <h2 className="text-xl font-semibold mt-4">{event.name}</h2>
            <p>{event.description}</p>
            <p className="text-sm text-gray-600">Location: {event.location}</p>
            <p className="text-sm text-gray-600">Date: {event.date}</p>
            <p className="text-sm text-gray-600">Price: ${event.price}</p>
            <p className="text-sm text-gray-600">Available: {event.available_tickets}</p>

            <div className="qty-selector">
              <button onClick={() => updateQty(event.id, -1)}>-</button>
              <span>{quantities[event.id] || 1}</span>
              <button onClick={() => updateQty(event.id, 1)}>+</button>
            </div>

            <button onClick={() => handleBuy(event)} className="buy-button">
              Buy
            </button>
          </div>
        );
      })}
    </div>
  );
}

export default function EventCatalogApp() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">Browse Event Tickets</h1>
      <EventList />
    </div>
  );
}
