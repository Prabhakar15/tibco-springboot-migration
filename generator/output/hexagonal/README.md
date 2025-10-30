# TIBCO Migration - Hexagonal Architecture (COMBINED)

This project was generated using **Hexagonal Architecture** (Ports & Adapters pattern).

## Architecture Overview

```
Domain (Core Business Logic)
    ↑
Input Ports (Use Cases)
    ↑
Adapters (COMBINED)
```

## Project Structure

```
src/main/java/
├── domain/              # Core business logic (no dependencies)
│   ├── model/          # Domain entities
│   ├── port/
│   │   ├── input/      # Use case interfaces
│   │   └── output/     # Infrastructure interfaces
│   └── service/        # Business logic implementation
│
├── adapter/            # Adapters (depend on domain)
│   ├── input/
│   │   ├── rest/       # REST controller
│   │   └── soap/       # SOAP endpoint
│   └── output/
│       ├── persistence/ # JPA adapter
│       ├── http/       # HTTP client adapter
│       └── messaging/  # JMS adapter
│
└── config/             # Spring configuration
```

## Build and Run

```bash
# Build
mvn clean package

# Run
mvn spring-boot:run
```

## Service URLs

### REST API
- Base URL: `http://localhost:8080/api/loans`
- Apply for loan: `POST /api/loans/apply`
- Get loan: `GET /api/loans/{{loanId}}`

### SOAP Web Service
- WSDL: `http://localhost:8081/ws/loanApplication.wsdl`
- Endpoint: `http://localhost:8081/ws`


## Key Features

- ✅ **Domain-Driven Design**: Pure domain model with no framework dependencies
- ✅ **Testable**: Business logic can be tested without infrastructure
- ✅ **Technology Independence**: Easy to swap JPA, REST, SOAP, etc.
- ✅ **Clear Boundaries**: Ports define explicit contracts
- ✅ **Single Responsibility**: Each adapter has one job

## Testing Strategy

1. **Unit Tests**: Test domain service with mock ports
2. **Integration Tests**: Test adapters with real infrastructure
3. **Contract Tests**: Verify port implementations

## Next Steps

1. Review generated code
2. Add business validation rules in domain service
3. Implement proper error handling
4. Add security (authentication/authorization)
5. Write tests for domain and adapters
