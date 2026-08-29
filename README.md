# Ecommerce Intelligence & Order Risk API

This repository contains a microservices-based system designed to fetch product and customer order details concurrently, evaluate risk parameters, and return transaction approval decisions.

---

## Architecture & Flowchart

The system is structured as a collection of distributed microservices communicating over HTTP. Below is a flowchart showing how data flows through the services when a risk evaluation request is sent:

```text
                          CLIENT / POSTMAN
                                 │
                                 ▼
                     ┌──────────────────────┐
                     │   API Requests       │
                     └──────────┬───────────┘
                                │
               ┌────────────────┼────────────────┐
               │                │                │
               ▼                ▼                ▼
         TASK 1              TASK 2           TASK 3
      Product API        Customer Order API   Combined Risk API
               │                │                │
               │                │                │
               ▼                ▼                ▼
        Product IDs        Customer ID       Customer ID
                          + Order ID          Order ID
                                              + Product IDs
               │                │                │
               ▼                ▼                │
        External Product   Queries 3 Mock APIs   │
             API              Concurrently:      │
               │         ┌──────┼──────┐         │
               │         ▼      ▼      ▼         │
               │      Customer Order History     │
               │        API    API    API        │
               │         │      │      │         │
               │         └──────┼──────┘         │
               │                ▼                │
               │          Customer Order         │
               │             Response            │
               │                                 │
               └──────────────┐   ┌──────────────┘
                              │   │
                              ▼   ▼
                        ┌─────────────────┐
                        │  asyncio.gather │
                        └────────┬────────┘
                                 │
                     Product API + Customer API
                        concurrently
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Risk Engine   │
                        └────────┬────────┘
                                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
                  ▼              ▼              ▼
              Customer       Product        Order Amount
               Status       Availability      Threshold
                  │              │              │
                  └──────────────┼──────────────┘
                                 │
                                 ▼
                            risk_score
                                 │
                                 ▼
                  ┌─────────────────────────┐
                  │        Decision         │
                  └────────────┬────────────┘
                               │
                   ┌───────────┼───────────┐
                   ▼           ▼           ▼
                APPROVED     REVIEW     REJECTED
                               │
                               ▼
                         Final Response
```

---

## Port Allocation

To resolve port conflicts and allow all services to run concurrently, the ports are allocated as follows:

| Service Name | Path/Endpoint | Port |
|---|---|---|
| **Product API** | `POST /products` | `8000` |
| **Customer API** (Mock) | `GET /customer/{customer_id}` | `8001` |
| **Order API** (Mock) | `GET /order/{order_id}` | `8002` |
| **History API** (Mock) | `GET /history/{customer_id}` | `8003` |
| **Customer Order API** | `POST /customer-order` | `8004` |
| **Risk API** (Gateway) | `POST /risk` | `8005` |

---


## How to Set Up and Run

### 1. Install Dependencies
Install the required packages using pip:
```bash
pip install -r requirments.txt
```

### 2. Launch Services Manually
Run the following commands in **6 separate terminal windows** (from the project root directory):

```bash
# Terminal 1: Product API (Port 8000)
python src/product/product_api.py

# Terminal 2: Customer API Mock (Port 8001)
python src/customer/external_api/customer_api.py

# Terminal 3: Order API Mock (Port 8002)
python src/customer/external_api/order_api.py

# Terminal 4: History API Mock (Port 8003)
python src/customer/external_api/history_api.py

# Terminal 5: Customer Order API Client (Port 8004)
python src/customer/httpx_client.py

# Terminal 6: Risk API Gateway (Port 8005)
python src/combine/risk_api.py
```

---

## How to Test

### Testing via Postman
You can test the risk evaluation gateway by sending a request to the Risk API:

- **Method**: `POST`
- **URL**: `http://localhost:8005/risk`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "customer_id": 501,
  "order_id": 9001,
  "product_ids": [1, 2, 3]
}
```

- **Example Response**:
```json
{
  "customer_id": 501,
  "order_id": 9001,
  "products": 3,
  "risk_score": 0,
  "decision": "APPROVED",
  "reason": [
    "Customer is active",
    "Product availability confirmed",
    "Order amount within threshold"
  ]
}
```
