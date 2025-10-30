# TIBCO BusinessWorks to Spring Boot Migration Framework

An AI-powered framework that automatically migrates TIBCO BusinessWorks processes to modern Spring Boot microservices (REST and SOAP).

## 🚀 Features

- **Multi-Agent AI Architecture**: LeaderAgent, ProcessAgent, RestServiceAgent, SoapServiceAgent, HexagonalServiceAgent, ValidationAgent, and Packager
- **Dual Architecture Support**: Choose between Layered (traditional) or Hexagonal (Ports & Adapters) patterns
- **API Gateway**: Spring Cloud Gateway for unified entry point with routing, circuit breaker, rate limiting, CORS
- **Automatic Code Generation**: Converts TIBCO `.process` files to complete Spring Boot projects
- **REST Service Generation**: Controllers, DTOs, Services, JPA Entities, Repositories
- **SOAP Service Generation**: Spring-WS endpoints, WSDL configuration, JAXB marshalling
- **Hexagonal Architecture**: Domain-driven design with clean separation, pure domain logic, testable without Spring
- **XSD Integration**: Parses and integrates XSD schemas with JAXB
- **Database Support**: JPA/Hibernate with H2 (dev) and Oracle (production)
- **JMS Integration**: Apache Artemis for messaging
- **RAG-Based Intelligence**: ProcessKnowledgeBase for context-aware code generation
- **Packaging**: Automatic ZIP archive creation for deployable projects

## 📋 Prerequisites

- Python 3.8+
- Java 17+ (for running generated Spring Boot services)
- Maven 3.6+ (for building generated projects)
- Git (for version control)

## 🛠️ Quick Start

### 1. Setup Environment (PowerShell on Windows)

```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Migration

#### Option A: Layered Architecture (Default)
```powershell
cd generator
python -m generator.ai.run --input-dir input_artifacts --output-dir output
```

Generates separate REST and SOAP projects with traditional layered structure.

#### Option B: Hexagonal Architecture (Ports & Adapters)
```powershell
cd generator
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output \
  --architecture hexagonal \
  --service-type combined  # or 'rest' or 'soap'
```

Generates single project with domain-driven design and clean architecture.

### 3. Access Generated Projects

**Layered Architecture (Default):**
- **REST Service**: `generator/output/rest/` (also `src_rest.zip`)
- **SOAP Service**: `generator/output/soap/` (also `src_soap.zip`)

**Hexagonal Architecture:**
- **Unified Service**: `generator/output/hexagonal/` (also `hexagonal_combined.zip`)
  - Contains domain layer, ports, and adapters (REST/SOAP/JPA/HTTP/JMS)

### 4. Build and Run Generated Services

```powershell
# REST Service (Layered)
cd generator/output/rest
mvn clean package
java -jar target/*.jar

# SOAP Service (Layered)
cd generator/output/soap
mvn clean package
java -jar target/*.jar

# Hexagonal Service (Unified)
cd generator/output/hexagonal
mvn clean package
java -jar target/*.jar
# Access REST at http://localhost:8080/api/loans/apply
# Access SOAP WSDL at http://localhost:8080/ws/loanApplication.wsdl
```

## 🏗️ Architecture Options

The framework supports **two architectural patterns**:

### Layered Architecture (Default)
Traditional Spring Boot structure:
```
rest/                           soap/
├── controller/                 ├── endpoint/
├── service/                    ├── service/
├── repository/                 ├── repository/
├── entity/                     ├── entity/
└── dto/                        └── dto/
```

**Best for:** Standard CRUD, quick prototypes, teams familiar with Spring Boot

### Hexagonal Architecture (Ports & Adapters)
Domain-driven design with clean architecture:
```
hexagonal/
├── domain/                     # Pure business logic (NO framework deps)
│   ├── model/                  # Business entities
│   ├── port/
│   │   ├── in/                 # Use case interfaces
│   │   └── out/                # Repository interfaces
│   └── service/                # Domain service
└── adapter/
    ├── in/                     # Input adapters
    │   ├── rest/               # REST controller
    │   └── soap/               # SOAP endpoint
    └── out/                    # Output adapters
        ├── persistence/        # JPA adapter
        ├── http/               # HTTP gateway
        └── jms/                # JMS adapter
```

**Best for:** Complex business logic, high testability, technology independence, DDD

### Comparison

| Feature | Layered | Hexagonal |
|---------|---------|-----------|
| **Structure** | Controller → Service → Repository | Domain ← Adapters |
| **Domain Purity** | Mixed with framework | Zero framework deps |
| **Testability** | Requires Spring mocks | Pure unit tests |
| **Technology Coupling** | Tight | Loose (via interfaces) |
| **Projects Generated** | Separate REST/SOAP | Single unified project |
| **Complexity** | Lower | Higher |
| **Flexibility** | Good | Excellent |

### Usage Examples

#### Generate Layered (Default)
```bash
python -m generator.ai.run --input-dir input_artifacts --output-dir output
```

#### Generate Hexagonal with Both REST and SOAP
```bash
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output \
  --architecture hexagonal \
  --service-type combined
```

#### Generate Hexagonal with REST Only
```bash
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output \
  --architecture hexagonal \
  --service-type rest
```

**See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed hexagonal architecture documentation.**

## 🌐 API Gateway (Spring Cloud Gateway)

Generate a **Spring Cloud Gateway** as a single entry point for all microservices:

```bash
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output \
  --architecture hexagonal \
  --service-type combined \
  --gateway
```

The gateway provides:
- **Unified Entry Point**: Single endpoint at `http://localhost:8080`
- **Path-Based Routing**: `/api/{service}/**` (REST), `/ws/{service}/**` (SOAP)
- **Circuit Breaker**: Fault tolerance with Resilience4j
- **Rate Limiting**: Prevent API abuse with Redis
- **CORS**: Cross-origin resource sharing
- **Load Balancing**: Distribute traffic across instances
- **Monitoring**: Actuator endpoints for health checks

### Generated Structure
```
output/
├── api-gateway/              # Spring Cloud Gateway
│   ├── pom.xml
│   ├── README.md
│   └── src/
│       └── main/
│           ├── java/
│           │   └── gateway/
│           │       ├── ApiGatewayApplication.java
│           │       ├── config/
│           │       │   ├── GatewayConfig.java
│           │       │   ├── RouteConfig.java      # Auto-configured routes
│           │       │   └── CorsConfig.java
│           │       └── filter/
│           │           └── LoggingGatewayFilterFactory.java
│           └── resources/
│               └── application.yml
├── LoanApplicationProcess_hexagonal_combined.zip
└── api-gateway.zip
```

### Gateway Routes (Auto-configured)

| Service | Type | Gateway Path | Backend |
|---------|------|--------------|---------|
| LoanApplication | Hexagonal (REST) | `/api/loanapplication/**` | `http://localhost:8081` |
| LoanApplication | Hexagonal (SOAP) | `/ws/loanapplication/**` | `http://localhost:8081` |

### Usage Example
```bash
# Start backend service
cd output/hexagonal
mvn spring-boot:run  # Runs on port 8081

# Start API Gateway (in new terminal)
cd output/api-gateway
mvn spring-boot:run  # Runs on port 8080

# Access via gateway
curl http://localhost:8080/api/loanapplication/loans/apply
```

**See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for complete gateway documentation.**

## 📁 Project Structure

```
tibco_migration/
├── generator/
│   ├── generator/
│   │   ├── ai/                    # AI agents
│   │   │   ├── leader.py          # Orchestrates migration
│   │   │   ├── process_agent.py   # Handles process parsing
│   │   │   ├── service_agents.py  # REST/SOAP generation (layered)
│   │   │   ├── hexagonal_agents.py # Hexagonal architecture generation
│   │   │   ├── validation_agent.py # Validates output
│   │   │   ├── packager.py        # Creates ZIP archives
│   │   │   ├── rag.py             # RAG knowledge base
│   │   │   └── run.py             # CLI entry point
│   │   ├── process_parser.py      # Parses .process files
│   │   ├── xsd_parser.py          # Parses XSD schemas
│   │   └── templates.py           # Code templates
│   ├── input_artifacts/           # TIBCO process files
│   └── output/                    # Generated projects
│       ├── rest/                  # Spring Boot REST (layered)
│       ├── soap/                  # Spring Boot SOAP (layered)
│       ├── hexagonal/             # Hexagonal architecture (if selected)
│       ├── src_rest.zip
│       ├── src_soap.zip
│       └── hexagonal_*.zip
├── MIGRATION_GUIDE.md             # Comprehensive documentation
├── MIGRATION_GUIDE.html           # HTML version
└── requirements.txt               # Python dependencies
```

## 🎯 Input Requirements

Place your TIBCO artifacts in `generator/input_artifacts/`:

- `.process` files (TIBCO BusinessWorks processes)
- `.xsd` files (XML schemas)
- Connection configuration files (`jdbc_connection.xml`, `jms_connection.xml`)

## 📊 Generated Spring Boot Components

### REST Service
- Controllers with `@RestController`
- DTOs with validation annotations
- JPA entities and repositories
- Service layer with business logic
- XSD-based JAXB classes
- WebClient for external API calls
- Complete `pom.xml` with all dependencies

### SOAP Service
- `@Endpoint` with `@PayloadRoot` annotations
- WebServiceConfig with WSDL generation
- JAXB-annotated request/response DTOs
- XSD schemas with unified namespace
- Spring-WS configuration
- Complete `pom.xml` with spring-boot-starter-web-services

## 📖 Documentation

For detailed documentation, architecture diagrams, and examples, see:
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Complete guide with sequence diagrams
- **[MIGRATION_GUIDE.html](MIGRATION_GUIDE.html)** - HTML version for PDF export

## 🧪 Testing

```powershell
# Run Python tests
python -m pytest -v

# Test generated REST service
cd generator/output/rest
mvn test

# Test generated SOAP service
cd generator/output/soap
mvn test
```

## 🔧 Configuration

### Python Dependencies
See `requirements.txt` for required packages.

### Generated Service Configuration
- REST: `generator/output/rest/src/main/resources/application.yml`
- SOAP: `generator/output/soap/src/main/resources/application.yml`

### 🤖 AI-Powered Generation (Optional)

The framework currently uses **template-based code generation** (fast, no API costs). You can optionally enable **AI-powered generation**:

#### Enable AI Features:

```powershell
# 1. Install AI dependencies
pip install openai sentence-transformers faiss-cpu numpy

# 2. Set OpenAI API key
$env:OPENAI_API_KEY="sk-your-api-key-here"

# 3. RAG vector database now works automatically!
```

**What changes:**
- ✅ RAG module (`rag.py`) switches from fallback to AI mode automatically
- ✅ Vector database (FAISS) indexes TIBCO activities for similarity search
- ✅ No code changes needed - just install dependencies!

**AI vs Template:**

| Mode | Speed | Cost | Intelligence |
|------|-------|------|--------------|
| Template (default) | Very Fast | $0 | Fixed patterns |
| AI-powered | Slower | ~$0.12/service | Context-aware |

**When to use AI:**
- Complex TIBCO processes with unique patterns
- Need intelligent activity mapping
- Want to leverage historical migration knowledge

See **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** section "Enabling AI-Powered Code Generation" for full details.

## 📦 Technology Stack
- SOAP: `generator/output/soap/src/main/resources/application.yml`

## 📦 Technology Stack

### Framework
- Python 3.13+
- OpenAI API (for AI-powered generation)
- ChromaDB (for RAG vector store)

### Generated Services
- Spring Boot 3.2.0
- Java 17
- Spring Web / Spring Web Services
- Spring Data JPA
- Apache Artemis (JMS)
- JAXB 3.x
- Maven

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **Prabhakara Rao Inapanuri** - [GitHub](https://github.com/Prabhakar15)

## 🌟 Acknowledgments

- Built with AI-powered code generation
- Supports TIBCO BusinessWorks 5.x/6.x migration patterns
- Enterprise-ready Spring Boot architecture
