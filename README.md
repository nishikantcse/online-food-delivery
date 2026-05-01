# online-food-delivery
Scalable Services Assignment


🧠 Recommended Approach: “Structured Monorepo (Microservices-ready)”

Even though the assignment says separate repositories, you can:

Develop everything in one repo (for submission & ease)
Structure it such that each service is independent & deployable
Later explain: “Designed as independent services, organized in mono-repo for development efficiency”
📁 Suggested Git Repository Structure
online-food-delivery/
│
├── services/
│   ├── customer-service/
│   ├── restaurant-service/
│   ├── order-service/
│   ├── payment-service/
│   ├── delivery-service/
│   └── notification-service/ (optional)
│
├── shared/
│   ├── api-gateway/ (optional)
│   ├── common-utils/
│   ├── contracts/ (OpenAPI specs)
│
├── data/
│   ├── seed-data/
│   │   ├── customers.csv
│   │   ├── restaurants.csv
│   │   └── ...
│   └── db-init-scripts/
│
├── infra/
│   ├── docker/
│   │   ├── docker-compose.yml
│   ├── k8s/
│   │   ├── customer/
│   │   ├── order/
│   │   └── ...
│
├── observability/
│   ├── prometheus/
│   ├── grafana/
│   └── dashboards/
│
├── docs/
│   ├── architecture.md
│   ├── context-map.md
│   ├── er-diagrams/
│
├── scripts/
│   ├── setup.sh
│   └── seed.sh
│
├── README.md
└── .env
🔧 Each Microservice Structure (Standardized)

Example: order-service/

order-service/
│
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── repositories/
│   └── schemas/
│
├── migrations/
├── tests/
├── Dockerfile
├── requirements.txt (FastAPI)
└── README.md

Since you mentioned earlier:
👉 React + FastAPI + PostgreSQL
Stick with that — it’s perfect for this assignment.

🧩 Service Breakdown (Mapping from Assignment)

Based on your file:

1. Customer Service
DB: customers, addresses
APIs:
POST /customers
GET /customers
POST /addresses
2. Restaurant Service
DB: restaurants, menu_items
APIs:
GET /restaurants
GET /menu
PATCH /availability
3. Order Service ⭐ (Core Logic)
DB: orders, order_items
Responsibilities:
Validate restaurant open
Validate item availability
Apply rules:
max 20 items
qty ≤ 5
Calculate total
4. Payment Service
DB: payments, idempotency_keys
APIs:
POST /charge (Idempotency-Key REQUIRED)
POST /refund
5. Delivery Service
DB: drivers, deliveries
Flow:
ASSIGNED → PICKED → DELIVERED
6. Notification Service (Optional but boosts marks)
Logs notifications
Simulate email/SMS
🔗 Inter-Service Communication Design
Synchronous Flow (MANDATORY)
Client → Order Service
        → Restaurant Service (validate)
        → Payment Service (charge)
        → Delivery Service (assign)
        → Notification Service
💡 Best Practice (Mention in Viva)
Use API composition
Avoid shared DB
Use replicated fields like:
restaurant_name in orders
city in order
🐳 Docker Strategy
Root docker-compose.yml
services:
  customer-service:
  order-service:
  payment-service:
  restaurant-service:
  delivery-service:
  
  postgres-customer:
  postgres-order:
  postgres-payment:

👉 Each service has its own DB → database-per-service ✅

☸️ Kubernetes (Minikube)

Inside /infra/k8s/:

customer/
  deployment.yaml
  service.yaml
  configmap.yaml
  secret.yaml

Repeat for each service.

📊 Observability Plan (Very Important for Marks)
Metrics:
orders_placed_total
payment_failures_total
request_latency_ms
Stack:
Prometheus
Grafana
🧾 Documentation (Scoring Section)

Inside /docs/:

Must include:
✅ ER diagrams per service
✅ Context map
✅ API contracts (OpenAPI)
✅ Workflow diagram
⚡ Development Plan (Step-by-Step)
Phase 1 – Setup (Day 1)
Create repo + folder structure
Setup FastAPI template for all services
Phase 2 – Core Services (Day 2–3)
Customer Service
Restaurant Service
Phase 3 – Order + Payment (Day 4–5)
Order Service (business rules)
Payment (idempotency)
Phase 4 – Delivery + Notification (Day 6)
Delivery flow
Notification logging
Phase 5 – Infra (Day 7)
Docker + Compose
Minikube setup
Phase 6 – Observability (Day 8)
Prometheus + Grafana
💡 Pro Tips (Very Important for Evaluation)
Add correlationId in every request
Use structured logs (JSON)
Implement:
retries
timeouts
Show failure scenarios (payment fail)
🚀 Bonus (To Impress Evaluator)
Add API Gateway (optional)
Add Swagger UI for each service
Add Postman collection