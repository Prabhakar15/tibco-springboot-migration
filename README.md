# TIBCO BusinessWorks to Spring Boot Migration Framework

An AI-powered framework that automatically migrates TIBCO BusinessWorks processes to modern Spring Boot microservices (REST and SOAP).

## 🚀 Features

- **Multi-Agent AI Architecture**: LeaderAgent, ProcessAgent, RestServiceAgent, SoapServiceAgent, ValidationAgent, and Packager
- **Automatic Code Generation**: Converts TIBCO `.process` files to complete Spring Boot projects
- **REST Service Generation**: Controllers, DTOs, Services, JPA Entities, Repositories
- **SOAP Service Generation**: Spring-WS endpoints, WSDL configuration, JAXB marshalling
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

```powershell
# Navigate to generator directory
cd generator

# Run the AI-based migration
python -m generator.ai.run --input-dir input_artifacts --output-dir output
```

### 3. Access Generated Projects

The framework generates two Spring Boot projects:

- **REST Service**: `generator/output/rest/` (also packaged as `src_rest.zip`)
- **SOAP Service**: `generator/output/soap/` (also packaged as `src_soap.zip`)

### 4. Build and Run Generated Services

```powershell
# REST Service
cd generator/output/rest
mvn clean package
java -jar target/*.jar

# SOAP Service (in new terminal)
cd generator/output/soap
mvn clean package
java -jar target/*.jar
```

## 📁 Project Structure

```
tibco_migration/
├── generator/
│   ├── generator/
│   │   ├── ai/                    # AI agents
│   │   │   ├── leader.py          # Orchestrates migration
│   │   │   ├── process_agent.py   # Handles process parsing
│   │   │   ├── service_agents.py  # REST/SOAP generation
│   │   │   ├── validation_agent.py # Validates output
│   │   │   ├── packager.py        # Creates ZIP archives
│   │   │   ├── rag.py             # RAG knowledge base
│   │   │   └── run.py             # CLI entry point
│   │   ├── process_parser.py      # Parses .process files
│   │   ├── xsd_parser.py          # Parses XSD schemas
│   │   └── templates.py           # Code templates
│   ├── input_artifacts/           # TIBCO process files
│   └── output/                    # Generated projects
│       ├── rest/                  # Spring Boot REST
│       ├── soap/                  # Spring Boot SOAP
│       ├── src_rest.zip
│       └── src_soap.zip
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
