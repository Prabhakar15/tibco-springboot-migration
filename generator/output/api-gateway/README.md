# API Gateway

Spring Cloud Gateway providing a single entry point for all microservices.

## Overview

This API Gateway acts as a reverse proxy and routes requests to appropriate backend services based on path patterns. It provides cross-cutting concerns like:

- **Routing**: Path-based and header-based routing
- **Load Balancing**: Distribute traffic across service instances
- **Circuit Breaker**: Fault tolerance with Resilience4j
- **Rate Limiting**: Prevent API abuse
- **CORS**: Cross-origin resource sharing
- **Monitoring**: Actuator endpoints for health checks
- **Logging**: Request/response tracking

## Architecture

```
┌─────────────┐
│   Clients   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│       API Gateway (Port 8080)       │
│  - Routing                          │
│  - Circuit Breaker                  │
│  - Rate Limiting                    │
│  - CORS                             │
└──────┬──────────────────────────────┘
       │
       ├──────────────┬──────────────┬────────────...
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ REST Service│ │ SOAP Service│ │  Hexagonal  │
│  (Layered)  │ │  (Layered)  │ │   Service   │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Quick Start

### 1. Build the Gateway

```bash
mvn clean package
```

### 2. Run the Gateway

```bash
java -jar target/api-gateway-1.0.0.jar
```

The gateway will start on port **8080**.

### 3. Start Backend Services

Ensure all backend services are running on their configured ports before starting the gateway.

## Configured Routes

| Service | Type | Gateway Path | Backend Port |
|---------|------|--------------|--------------|
| LoanApplicationProcess | Hexagonal (Combined) | `/api/loanapplicationprocess/**` (REST)<br>`/ws/loanapplicationprocess/**` (SOAP) | 8081 |

## Usage Examples

### REST Service Request

```bash
# Through gateway
curl http://localhost:8080/api/loanapplication/loans/123

# This routes to backend service at configured port
```

### SOAP Service Request

```bash
# Through gateway
curl -X POST http://localhost:8080/ws/loanapplication/service \
  -H "Content-Type: text/xml" \
  -d @request.xml
```

### Health Check

```bash
# Gateway health
curl http://localhost:8080/actuator/health

# All routes
curl http://localhost:8080/actuator/gateway/routes
```

## Features

### Circuit Breaker

Each route is protected with a circuit breaker:
- **Sliding Window Size**: 10 calls
- **Failure Rate Threshold**: 50%
- **Wait Duration in Open State**: 10 seconds
- **Half-Open Permitted Calls**: 3

### Rate Limiting

Configure rate limiting per route in `application.yml`:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: my_service
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
```

### CORS

CORS is configured globally to allow:
- All origins (customize for production)
- Common HTTP methods
- Custom headers
- Credentials

### Retry Mechanism

Failed requests are automatically retried up to 3 times before triggering the circuit breaker.

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_PORT` | Gateway port | 8080 |
| `REDIS_HOST` | Redis host for rate limiting | localhost |
| `REDIS_PORT` | Redis port | 6379 |

### Application Properties

Edit `src/main/resources/application.yml` to customize:
- Route definitions
- Circuit breaker settings
- Rate limiting
- CORS policies
- Timeouts

## Monitoring

### Actuator Endpoints

- **Health**: `http://localhost:8080/actuator/health`
- **Gateway Routes**: `http://localhost:8080/actuator/gateway/routes`
- **Metrics**: `http://localhost:8080/actuator/metrics`

### Logging

Logs include:
- Request method and URI
- Response status codes
- Circuit breaker state changes
- Rate limiting events

## Production Considerations

1. **CORS**: Restrict `allowedOrigins` to specific domains
2. **Rate Limiting**: Enable Redis and configure appropriate limits
3. **SSL/TLS**: Configure HTTPS for secure communication
4. **Authentication**: Add authentication filters
5. **Service Discovery**: Integrate with Eureka/Consul for dynamic service discovery
6. **Distributed Tracing**: Add Spring Cloud Sleuth for request tracking

## Troubleshooting

### Route Not Found (404)

- Verify backend service is running
- Check route configuration in `RouteConfig.java`
- Review gateway logs for routing details

### Circuit Breaker Open

- Check backend service health
- Review circuit breaker metrics in Actuator
- Adjust threshold/timeout in `application.yml`

### CORS Errors

- Verify `CorsConfig.java` allows required origins
- Check browser console for specific CORS errors
- Ensure preflight requests (OPTIONS) are handled

## Dependencies

- **Spring Cloud Gateway**: 2022.0.4
- **Spring Boot**: 3.1.5
- **Resilience4j**: Circuit breaker
- **Redis**: Rate limiting (optional)

## License

Auto-generated by TIBCO BW to Spring Boot Migration Tool
