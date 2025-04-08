# Anti-Pattern Microservice Demo

This is a demonstration microservice designed to show what **NOT** to do when handling sensitive customer data or deploying across multiple regions. 

## Anti-Patterns Demonstrated

### 1. Lack of Redundancy and High Availability
- Single instance deployment with no failover
- Local SQLite database with no replication
- No use of multiple zones/regions for deployment

### 2. Avoiding Cloud Vendor-Specific Services
- Uses a local SQLite database instead of cloud databases like Azure SQL, Azure Cosmos DB, etc.
- Runs on a standalone server rather than cloud services like Azure App Service
- No use of managed security services

### 3. Poor Configuration Management
- Hardcoded database credentials directly in code
- No use of environment variables, Azure Key Vault, or encrypted connection strings
- No separation of configuration between environments

### 4. Absence of Centralized Monitoring
- Uses basic print statements instead of a logging framework
- No integration with monitoring services
- No metrics collection or alerting
- No tracing or distributed logging

### 5. Additional Security Issues
- Storing sensitive data (SSN, credit card) in plain text
- Returning sensitive data in API responses
- No input validation
- Exposing detailed error information
- No HTTPS

## Running the Service

### Prerequisites
- Python 3.6+

### Installation
1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running Locally
```
python app.py
```

The service will be available at http://localhost:5000

### API Endpoints

- `GET /health` - Basic health check
- `POST /customers` - Add a new customer
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "ssn": "123-45-6789",
    "credit_card": "4111111111111111"
  }
  ```
- `GET /customers` - Get all customers (with their sensitive data)
- `POST /admin` - Admin login
  ```json
  {
    "username": "admin",
    "password": "password123"
  }
  ```

## IMPORTANT DISCLAIMER

This service is **FOR DEMONSTRATION PURPOSES ONLY**. It intentionally contains serious security flaws and should **NEVER** be used in a production environment or with real customer data.

The anti-patterns demonstrated here are for educational purposes to show what practices to avoid when building real microservices that handle sensitive data. 