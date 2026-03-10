# Quick Start Guide - Bookstore Microservices

## What's New? 🎉
Created **8 new microservices** to complete your bookstore platform:
- order-service, pay-service, ship-service, staff-service
- manager-service, catalog-service, comment-rate-service, recommender-ai-service

Total: **12 services** ready to deploy!

## Quick Start

### 1. Start All Services
```bash
cd c:\bookstore-microservice
docker-compose up --build
```

### 2. Wait for Services to Initialize
All 12 services will start and be available on:
- API Gateway: `http://localhost:8000`
- Other services: ports 8001-8011

### 3. Access Service APIs
Example - View all orders:
```bash
curl http://localhost:8004/api/orders/
```

## Service Endpoints Quick Reference

| Service | Base URL | Main Endpoint |
|---------|----------|---------------|
| Order | localhost:8004 | `/api/orders/` |
| Payment | localhost:8005 | `/api/payments/` |
| Shipping | localhost:8006 | `/api/shipments/` |
| Staff | localhost:8007 | `/api/staff/` |
| Manager | localhost:8008 | `/api/managers/` |
| Catalog | localhost:8009 | `/api/categories/` |
| Reviews | localhost:8010 | `/api/reviews/` |
| Recommendations | localhost:8011 | `/api/recommendations/` |

## Service Features

### Order Service (8004)
- Create, retrieve, update orders
- Status tracking: pending, processing, shipped, delivered, cancelled
- Customer and total amount tracking

### Payment Service (8005)
- Payment processing
- Support for: Credit Card, Debit Card, PayPal, Bank Transfer
- Status tracking: pending, processing, completed, failed, refunded

### Shipping Service (8006)
- Shipment tracking
- Carrier information
- Estimated delivery dates
- Statuses: pending, shipped, in transit, delivered

### Staff Service (8007)
- Employee management
- Position tracking
- Contact information

### Manager Service (8008)
- Manager profiles
- Department assignments
- Operational management

### Catalog Service (8009)
- Book categories
- Category descriptions
- Active/inactive status

### Comment & Rating Service (8010)
- Product reviews (1-5 stars)
- Customer comments
- Review moderation (approval workflow)

### Recommender AI Service (8011)
- AI-powered book recommendations
- Recommendation scoring
- Uses scikit-learn for ML algorithms

## Common Commands

### Create a Resource
```bash
curl -X POST http://localhost:8004/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{"order_number":"ORD001","customer_id":1,"total_amount":99.99,"status":"pending"}'
```

### Get All Resources
```bash
curl http://localhost:8004/api/orders/
```

### Get Specific Resource
```bash
curl http://localhost:8004/api/orders/1/
```

### Update Resource
```bash
curl -X PUT http://localhost:8004/api/orders/1/ \
  -H "Content-Type: application/json" \
  -d '{"status":"processing"}'
```

### Delete Resource
```bash
curl -X DELETE http://localhost:8004/api/orders/1/
```

## Documentation Files

- **COMPLETION_REPORT.md** - Detailed project summary
- **SERVICES_OVERVIEW.md** - Complete service documentation
- **.gitignore** - Git configuration for Python/Django projects
- **docker-compose.yml** - All 12 services configuration

## Next Steps
1. ✅ All services are created and dockerized
2. 📝 Configure your API Gateway routes (api-gateway/gateway/views.py)
3. 🗄️ Set up PostgreSQL for production databases
4. 🔐 Add authentication between services
5. 📊 Implement monitoring and logging
6. 🚀 Deploy to your infrastructure

## Troubleshooting

### Services won't start?
```bash
docker-compose logs <service-name>
```

### Want to rebuild everything?
```bash
docker-compose down
docker-compose up --build
```

### Check specific service logs
```bash
docker-compose logs -f order-service
```

## Architecture Overview
```
┌─────────────────────────────────────────────────┐
│  Client Application                              │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────▼──────────┐
        │  API Gateway      │
        │  (Port 8000)      │
        └────────┬──────────┘
                 │
    ┌────────────┴────────────┬──────────────┬─────────────────┐
    │                         │              │                 │
┌───▼───┐  ┌──────────┐  ┌──▼─────┐  ┌────▼────┐  ┌────────┐
│Books  │  │Customer  │  │ Cart   │  │ Orders  │  │Payments│
│ (8002)│  │  (8001)  │  │ (8003) │  │ (8004)  │  │ (8005) │
└───────┘  └──────────┘  └────────┘  └─────────┘  └────────┘

┌────────────┐  ┌──────────┐  ┌────────────┐  ┌──────────────┐
│ Shipping   │  │ Staff    │  │ Manager    │  │ Catalog      │
│  (8006)    │  │  (8007)  │  │  (8008)    │  │  (8009)      │
└────────────┘  └──────────┘  └────────────┘  └──────────────┘

┌────────────────┐  ┌──────────────────────┐
│  Reviews &     │  │  Recommendations     │
│  Ratings       │  │  (AI)                │
│  (8010)        │  │  (8011)              │
└────────────────┘  └──────────────────────┘
```

---
🎉 **Project Status**: COMPLETE - All 12 services ready for development!
