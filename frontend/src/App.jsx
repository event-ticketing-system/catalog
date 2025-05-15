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

  const handleBuy = async (event) => {
    const quantity = quantities[event.id];
    const payload = {
      event_id: String(event.id),
      event_name: event.name,
      quantity,
      price: event.price,
      total_price: event.price * quantity,
      order_time: new Date().toISOString(),
      user_id: "mock_user"
    };
  
    try {
      // Step 1: Create order
      const orderRes = await fetch("http://localhost:8002/api/orders/create", {
        method: "POST",
        credentials: 'include',
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });
  
      const orderData = await orderRes.json();
      const paymentUrl = orderData.payment_url;
  
      if (!paymentUrl) {
        alert("Payment URL not returned");
        return;
      }
  
      // Step 2: Call payment initiation API
      const payRes = await fetch(paymentUrl);
      const payData = await payRes.json();
  
      if (payData.payment_url) {
        // Step 3: Open PhonePe QR in new tab
        window.open(payData.payment_url, "_blank");
      } else {
        alert("Failed to get PhonePe payment URL");
      }
    } catch (err) {
      console.error("Payment flow failed", err);
      alert("Payment flow failed");
    }
  };
  

  if (loading) return <p>Loading events...</p>;

  return (
    <div className="event-container">
      {events.map((event) => {
        const imageSrc = event.image.startsWith("http")
          ? event.image
          : `http://localhost:8004${event.image}`;

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
      <h1 className="heading">
        <span role="img" aria-label="party">🎉</span>
        <span role="img" aria-label="popcorn">🍿</span>
        <span role="img" aria-label="ticket">🎟️</span>
        <span className="gradient-text"> Browse Event Tickets </span>
        <span role="img" aria-label="party">🎟️</span>
        <span role="img" aria-label="popcorn">🍿</span>
        <span role="img" aria-label="ticket">🎉</span>
      </h1>
      <EventList />
    </div>
  );
}
