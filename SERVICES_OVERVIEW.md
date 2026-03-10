# Bookstore Microservices Project - Service Overview

## Project Architecture

This is a microservices-based bookstore application built with Django REST Framework. The system is containerized using Docker and coordinated via Docker Compose.

## All Available Services (12 Total)

### 1. **API Gateway** (Port 8000)
- **Description**: Central entry point for all client requests
- **Routes**: Forwards requests to appropriate microservices
- **Location**: `api-gateway/`

### 2. **Customer Service** (Port 8001)
- **Description**: Manages customer information and user accounts
- **Models**: Customer profiles
- **Location**: `customer-service/`

### 3. **Book Service** (Port 8002)
- **Description**: Manages book inventory and metadata
- **Models**: Books with title, author, price, inventory
- **Location**: `book-service/`

### 4. **Cart Service** (Port 8003)
- **Description**: Handles shopping cart operations
- **Models**: Cart items management
- **Location**: `cart-service/`

### 5. **Order Service** (Port 8004) **[NEW]**
- **Description**: Manages customer orders and order lifecycle
- **Models**: Order with status tracking (pending, processing, shipped, delivered, cancelled)
- **Location**: `order-service/`

### 6. **Payment Service** (Port 8005) **[NEW]**
- **Description**: Handles payment processing and transactions
- **Models**: Payment records with multiple payment methods (credit card, debit card, PayPal, bank transfer)
- **Status**: pending, processing, completed, failed, refunded
- **Location**: `pay-service/`

### 7. **Shipping Service** (Port 8006) **[NEW]**
- **Description**: Manages shipment tracking and delivery
- **Models**: Shipment with tracking numbers and carrier info
- **Status**: pending, shipped, in transit, delivered
- **Location**: `ship-service/`

### 8. **Staff Service** (Port 8007) **[NEW]**
- **Description**: Manages staff/employee information
- **Models**: Staff profiles with position and contact details
- **Location**: `staff-service/`

### 9. **Manager Service** (Port 8008) **[NEW]**
- **Description**: Handles manager operations and business logic
- **Models**: Manager profiles with department assignments
- **Location**: `manager-service/`

### 10. **Catalog Service** (Port 8009) **[NEW]**
- **Description**: Manages book categories and catalog organization
- **Models**: Category with descriptions and active status
- **Location**: `catalog-service/`

### 11. **Comment & Rating Service** (Port 8010) **[NEW]**
- **Description**: Handles product reviews and customer ratings
- **Models**: Review/Rating with 1-5 star ratings and comments
- **Approval**: Supports review moderation workflow
- **Location**: `comment-rate-service/`

### 12. **Recommender AI Service** (Port 8011) **[NEW]**
- **Description**: Provides AI-powered book recommendations
- **Dependencies**: scikit-learn, numpy for ML algorithms
- **Models**: Recommendation with scoring and reasoning
- **Location**: `recommender-ai-service/`

## Running the Project

### Prerequisites
- Docker
- Docker Compose

### Start All Services
```bash
docker-compose up --build
```

### Access Services
- API Gateway: http://localhost:8000
- Customer Service: http://localhost:8001
- Book Service: http://localhost:8002
- Cart Service: http://localhost:8003
- Order Service: http://localhost:8004
- Payment Service: http://localhost:8005
- Shipping Service: http://localhost:8006
- Staff Service: http://localhost:8007
- Manager Service: http://localhost:8008
- Catalog Service: http://localhost:8009
- Comment/Rate Service: http://localhost:8010
- Recommender AI Service: http://localhost:8011

## Service Structure

Each microservice follows the same Django + DRF structure:

```
<service-name>/
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── manage.py               # Django management script
├── <service_name>/         # Django project folder
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
└── app/                   # Django application
    ├── __init__.py
    ├── models.py          # Data models
    ├── serializers.py     # DRF serializers
    ├── views.py           # API endpoints (ViewSets)
    ├── urls.py            # App-level URLs
    ├── admin.py           # Django admin configuration
    ├── apps.py            # App configuration
    ├── tests.py           # Unit tests
    └── migrations/        # Database migrations
```

## API Endpoints Pattern

All services follow RESTful conventions through Django REST Framework's DefaultRouter:

- `GET /api/<resource>/` - List all items
- `POST /api/<resource>/` - Create new item
- `GET /api/<resource>/<id>/` - Retrieve specific item
- `PUT /api/<resource>/<id>/` - Update item
- `DELETE /api/<resource>/<id>/` - Delete item

## Technology Stack
- **Framework**: Django + Django REST Framework
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Language**: Python 3.9
- **ML Libraries** (Recommender Service): scikit-learn, numpy

## Notes
- All services are configured with DEBUG=True (change for production)
- Each service has its own SQLite database
- For production, move to PostgreSQL with shared database or separate databases per service
- Update SECRET_KEY values in settings.py for each service before deploying
