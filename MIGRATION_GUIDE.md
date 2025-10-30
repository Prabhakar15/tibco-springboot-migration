# TIBCO BusinessWorks to Spring Boot Migration Guide

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Component Details](#component-details)
4. [Setup Instructions](#setup-instructions)
5. [Usage Examples](#usage-examples)
6. [Flow Diagrams](#flow-diagrams)
7. [Sequence Diagrams](#sequence-diagrams)
8. [Generated Outputs](#generated-outputs)
9. [Troubleshooting](#troubleshooting)
10. [Hexagonal Architecture Support](#hexagonal-architecture-support)
11. [API Gateway (Spring Cloud Gateway)](#api-gateway-spring-cloud-gateway)

---

## Overview

This project provides an **automated migration framework** to convert TIBCO BusinessWorks (BW) process definitions into modern Spring Boot microservices (REST and SOAP).

### Key Features
- ✅ Multi-agent AI architecture for intelligent code generation
- ✅ Parallel processing support for multiple BW processes
- ✅ Generates both REST and SOAP Spring Boot services
- ✅ Complete Spring Boot project structure with Maven configuration
- ✅ JAXB/XSD integration for type safety
- ✅ JPA/Hibernate for database operations
- ✅ JMS messaging support
- ✅ Automated packaging and archiving

### Technology Stack

**Input:** TIBCO BusinessWorks `.process`, `.xsd`, `.bwp` files

**Output:** Spring Boot 3.2.0 projects with:
- Java 17
- Spring Web / Spring Web Services
- Spring Data JPA
- Spring JMS (Apache Artemis)
- JAXB for XML marshalling
- H2/Oracle database support

---

## Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    TIBCO BW Migration System                     │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────┐
        │         LeaderAgent (Orchestrator)        │
        │  • Discovers BW process folders          │
        │  • Builds shared knowledge base (RAG)    │
        │  • Creates ProcessAgents                 │
        │  • Manages parallel execution            │
        │  • Generates reports & archives          │
        └──────────────────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
    ┌─────────────────────┐       ┌─────────────────────┐
    │   ProcessAgent      │       │   ProcessAgent      │
    │   (Process 1)       │       │   (Process 2)       │
    │                     │       │                     │
    │ • Parse .process    │       │ • Parse .process    │
    │ • Extract XSDs      │       │ • Extract XSDs      │
    │ • Detect service    │       │ • Detect service    │
    │   types             │       │   types             │
    │ • Coordinate agents │       │ • Coordinate agents │
    └─────────────────────┘       └─────────────────────┘
                │                             │
        ┌───────┴───────┐             ┌───────┴───────┐
        ▼               ▼             ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│RestService   │ │SoapService   │ │RestService   │ │SoapService   │
│Agent         │ │Agent         │ │Agent         │ │Agent         │
│              │ │              │ │              │ │              │
│• REST API    │ │• SOAP/WSDL   │ │• REST API    │ │• SOAP/WSDL   │
│• Controller  │ │• Endpoint    │ │• Controller  │ │• Endpoint    │
│• DTOs        │ │• JAXB DTOs   │ │• DTOs        │ │• JAXB DTOs   │
│• Service     │ │• Config      │ │• Service     │ │• Config      │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────┐
        │         Supporting Components             │
        ├──────────────────────────────────────────┤
        │  • ValidationAgent (Maven validation)    │
        │  • Packager (ZIP archive creation)       │
        │  • ProcessKnowledgeBase (RAG/AI)         │
        └──────────────────────────────────────────┘
```

### Multi-Agent Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                         Agent Hierarchy                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              LeaderAgent (Orchestrator)                   │ │
│  │  Responsibilities:                                        │ │
│  │  - Scan input directory for BW processes                 │ │
│  │  - Build shared RAG knowledge base                       │ │
│  │  - Create and manage ProcessAgents                       │ │
│  │  - Execute parallel/sequential processing                │ │
│  │  - Generate migration report                             │ │
│  │  - Create ZIP archives                                   │ │
│  └──────────────────────────────────────────────────────────┘ │
│                          │                                      │
│                          │ creates & delegates                  │
│                          ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │          ProcessAgent (Per BW Process)                    │ │
│  │  Responsibilities:                                        │ │
│  │  - Parse .process files (XML)                            │ │
│  │  - Extract activities (SQL, JMS, HTTP, etc.)             │ │
│  │  - Identify data schemas (XSD)                           │ │
│  │  - Detect service type (REST/SOAP)                       │ │
│  │  - Delegate to service-specific agents                   │ │
│  │  - Generate shared artifacts (entities, repos)           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                │                           │                    │
│                │ delegates                 │ delegates          │
│                ▼                           ▼                    │
│  ┌──────────────────────────┐  ┌──────────────────────────┐  │
│  │   RestServiceAgent       │  │   SoapServiceAgent       │  │
│  │   ──────────────────     │  │   ──────────────────     │  │
│  │   Generates:             │  │   Generates:             │  │
│  │   • @RestController      │  │   • @Endpoint            │  │
│  │   • @Service classes     │  │   • WebServiceConfig     │  │
│  │   • DTOs                 │  │   • JAXB-annotated DTOs  │  │
│  │   • application.yml      │  │   • XSD schemas          │  │
│  │   • pom.xml (REST deps)  │  │   • WSDL configuration   │  │
│  │   • README.md            │  │   • pom.xml (WS deps)    │  │
│  └──────────────────────────┘  │   • README.md            │  │
│                                 └──────────────────────────┘  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. LeaderAgent (`generator/ai/leader.py`)

**Purpose:** Orchestrates the entire migration process

**Key Methods:**
- `discover_bw_folders()` - Scans input directory for BW artifacts
- `build_shared_knowledge()` - Indexes processes into RAG knowledge base
- `create_process_agents()` - Instantiates ProcessAgent for each BW folder
- `execute()` - Main execution loop with parallel/sequential processing

**Configuration:**
```python
leader = LeaderAgent(
    input_base='input_artifacts',      # BW process folder
    output_base='output',               # Generated code output
    package_root='com.example.tibco',  # Java package
    parallel=True,                      # Enable parallel processing
    max_workers=4                       # Thread pool size
)
```

### 2. ProcessAgent (`generator/ai/process_agent.py`)

**Purpose:** Analyzes individual BW process and coordinates service generation

**Key Responsibilities:**
1. Parse `.process` files using `process_parser.py`
2. Extract activities (JDBC, JMS, HTTP, SOAP)
3. Identify XSD schemas
4. Determine service type (REST vs SOAP)
5. Generate shared artifacts:
   - JPA Entities
   - Spring Data Repositories
   - Service classes
   - DTOs

**Context Object:**
```python
class ProcessContext:
    folder: Path                    # BW process folder
    output_folder: Path             # Target output folder
    package_root: str               # Java package
    process_defs: List[Dict]        # Parsed process definitions
    activities: List[Dict]          # Extracted activities
    schemas: List[Path]             # XSD files
    jdbc_operations: List[Dict]     # Database operations
    jms_operations: List[Dict]      # JMS messaging
    http_calls: List[Dict]          # HTTP/REST calls
```

### 3. RestServiceAgent (`generator/ai/service_agents.py`)

**Purpose:** Generates Spring Boot REST API implementation

**Generated Files:**
```
rest/
├── pom.xml                                    # Maven with Spring Web
├── src/main/java/
│   └── com/example/tibco_migration/
│       ├── controller/
│       │   └── LoanApplicationController.java # @RestController
│       ├── service/
│       │   └── LoanApplicationService.java    # @Service
│       ├── repository/
│       │   └── LoanRepository.java            # JpaRepository
│       ├── entity/
│       │   └── LoanEntity.java                # JPA Entity
│       └── dto/
│           ├── LoanApplicationRequest.java
│           └── LoanApplicationResponse.java
└── src/main/resources/
    ├── application.yml                        # Spring config
    └── xsd/                                   # Schema files
```

### 4. SoapServiceAgent (`generator/ai/service_agents.py`)

**Purpose:** Generates Spring Boot SOAP Web Service (Spring-WS)

**Generated Files:**
```
soap/
├── pom.xml                                    # Maven with Spring-WS
├── src/main/java/
│   └── com/example/tibco_migration/
│       ├── SoapServiceApplication.java        # @SpringBootApplication
│       ├── config/
│       │   ├── WebServiceConfig.java          # WSDL/XSD configuration
│       │   └── WebClientConfig.java           # External service client
│       ├── endpoint/
│       │   └── LoanApplicationEndpoint.java   # @Endpoint
│       ├── service/
│       │   └── LoanApplicationService.java    # Business logic
│       ├── repository/
│       │   └── LoanRepository.java            # JpaRepository
│       ├── entity/
│       │   └── LoanEntity.java                # JPA Entity
│       └── dto/
│           ├── LoanApplicationRequest.java    # JAXB annotated
│           └── LoanApplicationResponse.java   # JAXB annotated
└── src/main/resources/
    ├── application.yml                        # Spring config (port 8081)
    └── xsd/
        └── loan_request.xsd                   # Unified schema
```

### 5. ProcessKnowledgeBase (`generator/ai/rag.py`)

**Purpose:** AI-enhanced process analysis using RAG (Retrieval-Augmented Generation)

**Capabilities:**
- Index process activities across multiple BW processes
- Query similar patterns (e.g., "SQL database operation")
- Provide context-aware suggestions
- Learn from existing implementations

**Fallback Mode:** When AI libraries (numpy, sklearn) are unavailable, uses simple logging

### 6. ValidationAgent (`generator/ai/validation_agent.py`)

**Purpose:** Validates generated Maven projects

**Checks:**
- Maven executable availability
- Compilation success (`mvn compile`)
- Test execution (optional)
- Dependency resolution

### 7. Packager (`generator/ai/packager.py`)

**Purpose:** Creates distributable ZIP archives

**Output Archives:**
- `src_rest.zip` - REST service source code
- `src_soap.zip` - SOAP service source code

---

## Setup Instructions

### Prerequisites

1. **Python Environment**
   ```bash
   Python 3.8 or higher
   ```

2. **Java Development Kit**
   ```bash
   Java 17 or higher
   ```

3. **Maven** (optional, for building generated projects)
   ```bash
   Maven 3.6+
   ```

### Installation

#### Step 1: Clone or Navigate to Project Directory
```bash
cd c:\IBM\DBS-TIBCO-SPRINGBOOT\PY29OCT\tibco_migration
```

#### Step 2: Set Up Python Virtual Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt
```

#### Step 3: Verify Directory Structure
```
tibco_migration/
├── generator/
│   ├── generator/
│   │   ├── ai/
│   │   │   ├── leader.py
│   │   │   ├── process_agent.py
│   │   │   ├── service_agents.py
│   │   │   ├── rag.py
│   │   │   ├── validation_agent.py
│   │   │   ├── packager.py
│   │   │   └── run.py
│   │   ├── process_parser.py
│   │   ├── xsd_parser.py
│   │   ├── templates.py
│   │   └── generate.py
│   ├── input_artifacts/          # Place TIBCO BW artifacts here
│   │   └── LoanApp/
│   │       ├── LoanApplication.process
│   │       ├── loan_request.xsd
│   │       └── loan_response.xsd
│   └── output/                   # Generated Spring Boot projects
│       ├── rest/
│       ├── soap/
│       ├── src_rest.zip
│       └── src_soap.zip
└── MIGRATION_GUIDE.md
```

---

## Usage Examples

### Example 1: Basic Migration

#### Input Structure
Place your TIBCO BW artifacts in `generator/input_artifacts/`:

```
input_artifacts/
└── LoanApp/
    ├── LoanApplication.process
    ├── loan_request.xsd
    ├── loan_response.xsd
    ├── creditscore_request.xsd
    └── creditscore_response.xsd
```

#### Run Migration
```powershell
cd generator
python -m generator.ai.run --input-dir input_artifacts --output-dir output
```

#### Output
```
output/
├── rest/
│   ├── pom.xml
│   ├── src/
│   └── target/
├── soap/
│   ├── pom.xml
│   ├── src/
│   └── target/
├── src_rest.zip
├── src_soap.zip
└── ai_migration_report.json
```

### Example 2: Multi-Process Migration

#### Input Structure
```
input_artifacts/
├── LoanApp/
│   ├── LoanApplication.process
│   └── *.xsd
├── CreditCheck/
│   ├── CreditCheckProcess.process
│   └── *.xsd
└── PaymentProcess/
    ├── Payment.process
    └── *.xsd
```

#### Run Migration
```powershell
python -m generator.ai.run --input-dir input_artifacts --output-dir output
```

The system will:
1. Discover all 3 BW process folders
2. Process them in parallel (if enabled)
3. Generate REST and SOAP services for each
4. Create consolidated output structure

### Example 3: Custom Configuration

#### Python Script
```python
from generator.ai.leader import LeaderAgent

# Custom configuration
leader = LeaderAgent(
    input_base='input_artifacts',
    output_base='output',
    package_root='com.mycompany.migration',
    parallel=True,
    max_workers=8  # More threads for faster processing
)

# Execute migration
report = leader.execute()

# Print summary
print(f"Processed {len(report['processed_folders'])} folders")
print(f"Generated {len(report['generated_files'])} files")
print(f"Created {len(report['archives'])} archives")
```

### Example 4: Building Generated Projects

#### Build REST Service
```powershell
cd output\rest
mvn clean package

# Run the service
java -jar target\tibco-migration-rest-0.1.0.jar
```

Access at: `http://localhost:8080`

#### Build SOAP Service
```powershell
cd output\soap
mvn clean package

# Run the service
java -jar target\tibco-migration-soap-0.1.0.jar
```

Access WSDL at: `http://localhost:8081/ws/loanApplication.wsdl`

### Example 5: Testing REST Service

#### Sample REST Request
```bash
curl -X POST http://localhost:8080/loan/apply \
  -H "Content-Type: application/json" \
  -d '{
    "customerID": "CUST001",
    "loanAmount": 50000,
    "loanType": "Personal",
    "loanTermMonths": 36,
    "applicantName": "John Doe",
    "contactEmail": "john.doe@example.com"
  }'
```

#### Expected Response
```json
{
  "loanID": "550e8400-e29b-41d4-a716-446655440000",
  "status": "APPROVED",
  "message": "Loan application approved",
  "approvedAmount": 50000
}
```

### Example 6: Testing SOAP Service

#### Sample SOAP Request
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:loan="http://example.com/tibco_migration/loan">
   <soapenv:Header/>
   <soapenv:Body>
      <loan:LoanApplicationRequest>
         <loan:customerID>CUST001</loan:customerID>
         <loan:loanAmount>50000</loan:loanAmount>
         <loan:loanType>Personal</loan:loanType>
         <loan:loanTermMonths>36</loan:loanTermMonths>
         <loan:applicantName>John Doe</loan:applicantName>
         <loan:contactEmail>john.doe@example.com</loan:contactEmail>
      </loan:LoanApplicationRequest>
   </soapenv:Body>
</soapenv:Envelope>
```

#### Using curl
```bash
curl -X POST http://localhost:8081/ws \
  -H "Content-Type: text/xml" \
  -H "SOAPAction: \"\"" \
  -d @request.xml
```

---

## Flow Diagrams

### Overall Migration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Migration Flow                              │
└─────────────────────────────────────────────────────────────────┘

START
  │
  ├─► [1] Scan Input Directory
  │     │
  │     ├─► Find folders with .process, .xsd, .bwp files
  │     │
  │     └─► Result: List of BW process folders
  │
  ├─► [2] Build Knowledge Base (RAG)
  │     │
  │     ├─► Parse all .process files
  │     │
  │     ├─► Index activities (SQL, JMS, HTTP, etc.)
  │     │
  │     └─► Create searchable index for pattern matching
  │
  ├─► [3] Create Process Agents
  │     │
  │     └─► One ProcessAgent per BW folder
  │
  ├─► [4] Execute Processing (Parallel/Sequential)
  │     │
  │     ├─► For each ProcessAgent:
  │     │     │
  │     │     ├─► Parse .process file
  │     │     │
  │     │     ├─► Extract activities & schemas
  │     │     │
  │     │     ├─► Detect service type (REST/SOAP)
  │     │     │
  │     │     ├─► Generate REST project (if applicable)
  │     │     │     │
  │     │     │     ├─► Controller
  │     │     │     ├─► Service
  │     │     │     ├─► Repository
  │     │     │     ├─► Entity
  │     │     │     ├─► DTOs
  │     │     │     └─► pom.xml
  │     │     │
  │     │     └─► Generate SOAP project (if applicable)
  │     │           │
  │     │           ├─► Endpoint
  │     │           ├─► WebServiceConfig
  │     │           ├─► Service
  │     │           ├─► JAXB DTOs
  │     │           └─► pom.xml
  │     │
  │     └─► Collect all generated files
  │
  ├─► [5] Validate Projects
  │     │
  │     ├─► Check Maven availability
  │     │
  │     └─► Run mvn compile (optional)
  │
  ├─► [6] Package Output
  │     │
  │     ├─► Create src_rest.zip
  │     │
  │     └─► Create src_soap.zip
  │
  └─► [7] Generate Migration Report
        │
        └─► ai_migration_report.json
              ├─► Processed folders
              ├─► Generated files
              ├─► Validation results
              └─► Archive paths

END
```

### Process Agent Decision Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              ProcessAgent Decision Logic                        │
└─────────────────────────────────────────────────────────────────┘

Process Folder Received
        │
        ▼
   Parse .process File
        │
        ├─► Extract Activities
        │     ├─► JDBC operations
        │     ├─► JMS send/receive
        │     ├─► HTTP invocations
        │     └─► SOAP calls
        │
        ├─► Extract Schemas (.xsd files)
        │
        └─► Analyze Service Type
              │
              ├─► Contains HTTP activities? ──► REST Service
              │
              ├─► Contains SOAP activities? ──► SOAP Service
              │
              └─► Default ──────────────────► Both REST & SOAP
                    │
                    ├─► Generate REST Project
                    │     └─► RestServiceAgent.generate()
                    │
                    └─► Generate SOAP Project
                          └─► SoapServiceAgent.generate()
```

---

## Sequence Diagrams

### Migration Execution Sequence

```
┌──────┐     ┌────────────┐     ┌──────────────┐     ┌────────────────┐     ┌────────────────┐
│ User │     │LeaderAgent │     │ProcessAgent  │     │RestService     │     │SoapService     │
│      │     │            │     │              │     │Agent           │     │Agent           │
└──┬───┘     └─────┬──────┘     └──────┬───────┘     └────────┬───────┘     └────────┬───────┘
   │               │                   │                      │                      │
   │ execute()     │                   │                      │                      │
   ├──────────────►│                   │                      │                      │
   │               │                   │                      │                      │
   │               │ discover_bw_folders()                    │                      │
   │               ├──────────┐        │                      │                      │
   │               │          │        │                      │                      │
   │               │◄─────────┘        │                      │                      │
   │               │ List[Path]        │                      │                      │
   │               │                   │                      │                      │
   │               │ build_shared_knowledge()                 │                      │
   │               ├──────────┐        │                      │                      │
   │               │          │        │                      │                      │
   │               │◄─────────┘        │                      │                      │
   │               │ RAG index created │                      │                      │
   │               │                   │                      │                      │
   │               │ create_process_agents()                  │                      │
   │               ├──────────────────►│                      │                      │
   │               │                   │ new ProcessAgent()   │                      │
   │               │                   │                      │                      │
   │               │ analyze()         │                      │                      │
   │               ├──────────────────►│                      │                      │
   │               │                   │ parse_process()      │                      │
   │               │                   ├─────────────┐        │                      │
   │               │                   │             │        │                      │
   │               │                   │◄────────────┘        │                      │
   │               │                   │ ProcessContext       │                      │
   │               │                   │                      │                      │
   │               │ detect_service_types()                   │                      │
   │               ├──────────────────►│                      │                      │
   │               │                   ├─────────────┐        │                      │
   │               │                   │             │        │                      │
   │               │                   │◄────────────┘        │                      │
   │               │◄──────────────────┤ ['rest','soap']      │                      │
   │               │                   │                      │                      │
   │               │                   │ generate()           │                      │
   │               │                   ├─────────────────────►│                      │
   │               │                   │                      │ Generate:            │
   │               │                   │                      │ • Controller         │
   │               │                   │                      │ • Service            │
   │               │                   │                      │ • DTOs               │
   │               │                   │                      │ • pom.xml            │
   │               │                   │◄─────────────────────┤                      │
   │               │                   │ files_map            │                      │
   │               │                   │                      │                      │
   │               │                   │ generate()                                  │
   │               │                   ├────────────────────────────────────────────►│
   │               │                   │                                             │
   │               │                   │                      │ Generate:            │
   │               │                   │                      │ • Endpoint           │
   │               │                   │                      │ • WebServiceConfig   │
   │               │                   │                      │ • JAXB DTOs          │
   │               │                   │                      │ • pom.xml            │
   │               │                   │◄────────────────────────────────────────────┤
   │               │                   │ files_map            │                      │
   │               │◄──────────────────┤                      │                      │
   │               │ all_files         │                      │                      │
   │               │                   │                      │                      │
   │               │ validate()        │                      │                      │
   │               ├──────────┐        │                      │                      │
   │               │          │        │                      │                      │
   │               │◄─────────┘        │                      │                      │
   │               │                   │                      │                      │
   │               │ package()         │                      │                      │
   │               ├──────────┐        │                      │                      │
   │               │          │        │                      │                      │
   │               │◄─────────┘        │                      │                      │
   │               │ ZIP files created │                      │                      │
   │               │                   │                      │                      │
   │◄──────────────┤ report            │                      │                      │
   │ Success       │                   │                      │                      │
   │               │                   │                      │                      │
```

### REST Service Request Flow

```
┌────────┐    ┌────────────┐    ┌─────────┐    ┌────────────┐    ┌──────┐    ┌──────┐
│ Client │    │ Controller │    │ Service │    │ Repository │    │  DB  │    │ JMS  │
└───┬────┘    └─────┬──────┘    └────┬────┘    └─────┬──────┘    └──┬───┘    └──┬───┘
    │               │                │                │              │           │
    │ POST /loan/apply               │                │              │           │
    ├──────────────►│                │                │              │           │
    │               │ applyForLoan() │                │              │           │
    │               ├───────────────►│                │              │           │
    │               │                │ save(entity)   │              │           │
    │               │                ├───────────────►│              │           │
    │               │                │                │ INSERT       │           │
    │               │                │                ├─────────────►│           │
    │               │                │                │◄─────────────┤           │
    │               │                │◄───────────────┤ entity       │           │
    │               │                │                │              │           │
    │               │                │ callCreditScore()             │           │
    │               │                ├──────────┐     │              │           │
    │               │                │          │     │              │           │
    │               │                │◄─────────┘     │              │           │
    │               │                │ score          │              │           │
    │               │                │                │              │           │
    │               │                │ update(entity) │              │           │
    │               │                ├───────────────►│              │           │
    │               │                │                │ UPDATE       │           │
    │               │                │                ├─────────────►│           │
    │               │                │                │◄─────────────┤           │
    │               │                │◄───────────────┤              │           │
    │               │                │                │              │           │
    │               │                │ sendJMS(status)│              │           │
    │               │                ├───────────────────────────────────────────►│
    │               │                │                │              │           │
    │               │◄───────────────┤ response       │              │           │
    │◄──────────────┤ JSON response  │                │              │           │
    │ 200 OK        │                │                │              │           │
```

### SOAP Service Request Flow

```
┌────────┐    ┌──────────┐    ┌─────────┐    ┌────────────┐    ┌──────┐    ┌──────┐
│ Client │    │ Endpoint │    │ Service │    │ Repository │    │  DB  │    │ JMS  │
└───┬────┘    └────┬─────┘    └────┬────┘    └─────┬──────┘    └──┬───┘    └──┬───┘
    │              │               │                │              │           │
    │ SOAP Request (XML)           │                │              │           │
    ├─────────────►│               │                │              │           │
    │              │ JAXB Unmarshal│                │              │           │
    │              ├──────┐        │                │              │           │
    │              │      │        │                │              │           │
    │              │◄─────┘        │                │              │           │
    │              │ Request DTO   │                │              │           │
    │              │               │                │              │           │
    │              │ applyForLoan()│                │              │           │
    │              ├──────────────►│                │              │           │
    │              │               │ save(entity)   │              │           │
    │              │               ├───────────────►│              │           │
    │              │               │                │ INSERT       │           │
    │              │               │                ├─────────────►│           │
    │              │               │                │◄─────────────┤           │
    │              │               │◄───────────────┤ entity       │           │
    │              │               │                │              │           │
    │              │               │ callCreditScore()             │           │
    │              │               ├──────────┐     │              │           │
    │              │               │          │     │              │           │
    │              │               │◄─────────┘     │              │           │
    │              │               │ score          │              │           │
    │              │               │                │              │           │
    │              │               │ update(entity) │              │           │
    │              │               ├───────────────►│              │           │
    │              │               │                │ UPDATE       │           │
    │              │               │                ├─────────────►│           │
    │              │               │                │◄─────────────┤           │
    │              │               │◄───────────────┤              │           │
    │              │               │                │              │           │
    │              │               │ sendJMS(status)│              │           │
    │              │               ├───────────────────────────────────────────►│
    │              │               │                │              │           │
    │              │◄──────────────┤ Response DTO   │              │           │
    │              │ JAXB Marshal  │                │              │           │
    │              ├──────┐        │                │              │           │
    │              │      │        │                │              │           │
    │              │◄─────┘        │                │              │           │
    │◄─────────────┤ SOAP Response │                │              │           │
    │ XML          │               │                │              │           │
```

---

## Generated Outputs

### REST Service Structure

```
output/rest/
│
├── pom.xml                          # Maven configuration
│   ├─ Spring Boot 3.2.0
│   ├─ spring-boot-starter-web
│   ├─ spring-boot-starter-data-jpa
│   ├─ spring-boot-starter-artemis
│   ├─ spring-boot-starter-webflux
│   └─ H2 database
│
├── src/main/java/com/example/tibco_migration/
│   │
│   ├── controller/
│   │   └── LoanApplicationController.java
│   │       ├─ @RestController
│   │       ├─ @RequestMapping("/loan")
│   │       └─ POST /loan/apply
│   │
│   ├── service/
│   │   └── LoanApplicationService.java
│   │       ├─ @Service
│   │       ├─ Business logic
│   │       ├─ Database operations
│   │       ├─ External API calls (WebClient)
│   │       └─ JMS messaging
│   │
│   ├── repository/
│   │   └── LoanRepository.java
│   │       ├─ extends JpaRepository<LoanEntity, String>
│   │       └─ Custom query methods
│   │
│   ├── entity/
│   │   └── LoanEntity.java
│   │       ├─ @Entity
│   │       ├─ @Table(name = "loans")
│   │       └─ JPA mappings
│   │
│   └── dto/
│       ├── LoanApplicationRequest.java
│       ├── LoanApplicationResponse.java
│       ├── CreditScoreRequest.java
│       └── CreditScoreResponse.java
│
└── src/main/resources/
    ├── application.yml              # Configuration
    │   ├─ server.port: 8080
    │   ├─ datasource (H2)
    │   ├─ JPA settings
    │   └─ JMS configuration
    │
    └── xsd/                         # Schema files
        ├── loan_request.xsd
        ├── loan_response.xsd
        ├── creditscore_request.xsd
        ├── creditscore_response.xsd
        └── bindings.xjb
```

### SOAP Service Structure

```
output/soap/
│
├── pom.xml                          # Maven configuration
│   ├─ Spring Boot 3.2.0
│   ├─ spring-boot-starter-web-services
│   ├─ spring-boot-starter-data-jpa
│   ├─ spring-boot-starter-artemis
│   ├─ spring-boot-starter-webflux
│   ├─ wsdl4j
│   ├─ jaxb2-maven-plugin
│   └─ H2 database
│
├── src/main/java/com/example/tibco_migration/
│   │
│   ├── SoapServiceApplication.java  # Main class
│   │   └─ @SpringBootApplication
│   │
│   ├── config/
│   │   ├── WebServiceConfig.java
│   │   │   ├─ @EnableWs
│   │   │   ├─ MessageDispatcherServlet (/ws/*)
│   │   │   ├─ WSDL definition (loanApplication)
│   │   │   └─ XSD schema configuration
│   │   │
│   │   └── WebClientConfig.java
│   │       └─ WebClient bean for external calls
│   │
│   ├── endpoint/
│   │   └── LoanApplicationEndpoint.java
│   │       ├─ @Endpoint
│   │       ├─ @PayloadRoot(namespace, localPart)
│   │       └─ @ResponsePayload
│   │
│   ├── service/
│   │   └── LoanApplicationService.java
│   │       └─ Business logic (same as REST)
│   │
│   ├── repository/
│   │   └── LoanRepository.java
│   │       └─ JpaRepository
│   │
│   ├── entity/
│   │   └── LoanEntity.java
│   │       └─ JPA entity
│   │
│   └── dto/
│       ├── LoanApplicationRequest.java
│       │   ├─ @XmlRootElement
│       │   ├─ @XmlAccessorType
│       │   └─ @XmlElement annotations
│       │
│       └── LoanApplicationResponse.java
│           └─ JAXB annotated
│
├── src/main/resources/
│   ├── application.yml              # Configuration
│   │   ├─ server.port: 8081
│   │   ├─ datasource (H2)
│   │   ├─ JPA settings
│   │   └─ JMS configuration
│   │
│   └── xsd/
│       └── loan_request.xsd         # Unified schema
│           ├─ LoanApplicationRequest element
│           └─ LoanApplicationResponse element
│
└── README.md                        # SOAP service documentation
```

### Migration Report (ai_migration_report.json)

```json
{
  "processed_folders": [
    "C:\\...\\input_artifacts\\LoanApp"
  ],
  "generated_files": [
    "C:\\...\\output\\src\\main\\java\\...\\Controller.java",
    "C:\\...\\output\\src\\main\\java\\...\\Service.java",
    "C:\\...\\output\\src\\main\\resources\\application.yml"
  ],
  "validation": {
    "C:\\...\\output\\rest": {
      "compiled": false,
      "mvn_available": false,
      "mvn_output": "Maven executable not found"
    },
    "C:\\...\\output\\soap": {
      "compiled": false,
      "mvn_available": false,
      "mvn_output": "Maven executable not found"
    }
  },
  "archives": [
    "C:\\...\\output\\src_rest.zip",
    "C:\\...\\output\\src_soap.zip"
  ]
}
```

---

## Troubleshooting

### Common Issues

#### 1. AI Libraries Not Available
**Error:**
```
AI libs not available (No module named 'numpy'); using fallback ProcessKnowledgeBase.
```

**Solution:**
This is normal. The system uses a fallback mode that works without AI libraries. If you want AI-enhanced features:
```bash
pip install numpy scikit-learn
```

#### 2. Maven Not Found
**Warning:**
```
Maven executable not found
```

**Solution:**
Install Maven or skip validation:
```bash
# Windows (Chocolatey)
choco install maven

# Or download from: https://maven.apache.org/download.cgi
```

#### 3. Port Already in Use
**Error:**
```
Port 8080 is already in use
```

**Solution:**
Change port in `application.yml`:
```yaml
server:
  port: 8090  # Use different port
```

#### 4. Database Connection Issues
**Error:**
```
Unable to obtain connection from database
```

**Solution:**
For H2 in-memory database (default), no action needed. For Oracle:
1. Uncomment Oracle dependency in `pom.xml`
2. Update `application.yml` with correct JDBC URL
3. Ensure Oracle driver is in classpath

#### 5. JAXB Classes Not Generated
**Error:**
```
Cannot find generated JAXB classes
```

**Solution:**
Run Maven with JAXB plugin:
```bash
mvn clean compile
```

This generates classes in `target/generated-sources/xjc/`

#### 6. WSDL Not Accessible
**Error:**
```
404 Not Found for /ws/loanApplication.wsdl
```

**Solution:**
1. Ensure SOAP service is running
2. Check `WebServiceConfig.java` bean name matches URL
3. Verify XSD file exists in `src/main/resources/xsd/`

### Debug Mode

Enable detailed logging:

**application.yml:**
```yaml
logging:
  level:
    org.springframework.ws: DEBUG
    com.example.tibco_migration: DEBUG
    org.springframework.jms: DEBUG
    org.springframework.data.jpa: DEBUG
```

---

## Advanced Topics

### Parallel Processing Configuration

```python
# Adjust parallel processing settings
leader = LeaderAgent(
    input_base='input_artifacts',
    output_base='output',
    package_root='com.example.tibco',
    parallel=True,        # Enable parallel processing
    max_workers=4         # Number of concurrent threads
)
```

**Guidelines:**
- `max_workers=1`: Sequential processing (safer, slower)
- `max_workers=4`: Good for 4-8 processes
- `max_workers=8`: For larger workloads (8+ processes)

### Custom Package Structure

```python
# Change Java package root
leader = LeaderAgent(
    input_base='input_artifacts',
    output_base='output',
    package_root='com.mycompany.integration'  # Custom package
)
```

Generated structure:
```
com/mycompany/integration/
├── controller/
├── service/
└── dto/
```

### Database Configuration

#### Oracle Database
**pom.xml:**
```xml
<dependency>
    <groupId>com.oracle.database.jdbc</groupId>
    <artifactId>ojdbc8</artifactId>
    <scope>runtime</scope>
</dependency>
```

**application.yml:**
```yaml
spring:
  datasource:
    url: jdbc:oracle:thin:@localhost:1521:XE
    username: your_username
    password: your_password
    driver-class-name: oracle.jdbc.OracleDriver
```

#### PostgreSQL
**pom.xml:**
```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

**application.yml:**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/loandb
    username: postgres
    password: postgres
```

### JMS Configuration

#### External ActiveMQ
**application.yml:**
```yaml
spring:
  artemis:
    mode: native
    broker-url: tcp://localhost:61616
    user: admin
    password: admin
```

#### JNDI-based JMS
```yaml
spring:
  jms:
    jndi-name: jms/ConnectionFactory
```

---

## Enabling AI-Powered Code Generation

The framework currently uses **template-based code generation** (fast, deterministic, no API costs). You can optionally enable **AI-powered generation** for more intelligent, context-aware code.

### Current Architecture

**Template-Based (Active):**
- Uses predefined Python string templates
- Fast and reliable
- No external dependencies
- Generates consistent, predictable code
- No API costs

**AI-Ready Design:**
- Multi-agent architecture ready for LLM integration
- RAG (Retrieval Augmented Generation) module already implemented
- Vector database (FAISS) support built-in
- Falls back to templates if AI libraries unavailable

### How to Enable AI Features

#### Step 1: Install AI Dependencies

Add to `requirements.txt`:
```python
# AI/ML Dependencies (optional)
openai==1.3.0              # For LLM API calls
sentence-transformers      # For embeddings
faiss-cpu                  # Vector database (use faiss-gpu for GPU)
numpy                      # Mathematical operations
```

Install:
```bash
pip install -r requirements.txt
```

**Note:** The `rag.py` module automatically detects these libraries and switches from fallback mode to AI mode!

#### Step 2: Set Up OpenAI API Key

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-api-key-here"

# Linux/Mac
export OPENAI_API_KEY="sk-your-api-key-here"
```

#### Step 3: Enable AI in Code (Future Enhancement)

The architecture supports adding AI with minimal changes:

**Option A: Enable RAG (Vector Search)**
```python
# Already works! Just install dependencies
from generator.ai.rag import ProcessKnowledgeBase

kb = ProcessKnowledgeBase()
kb.index_process_activities("input/LoanApplication.process")
similar = kb.query_similar_activities("SQL activity with parameterized query", k=5)
```

**Option B: Add LLM Code Generation (Enhancement)**

To add LLM-powered generation, enhance `service_agents.py`:

```python
from openai import OpenAI

class RestServiceAgent:
    def __init__(self, process_context, use_llm=False):
        self.ctx = process_context
        self.use_llm = use_llm
        if use_llm:
            self.llm_client = OpenAI()
    
    def generate(self):
        if self.use_llm:
            return self._generate_with_llm()
        else:
            return self._generate_with_templates()  # Current
    
    def _generate_with_llm(self):
        """Use LLM for intelligent code generation."""
        prompt = f"""
        Generate Spring Boot REST controller for:
        Process: {self.ctx.process_name}
        Activities: {self.ctx.activities}
        
        Requirements:
        - Use Spring Web annotations
        - Add validation
        - Include error handling
        - Follow best practices
        """
        
        response = self.llm_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_llm_response(response)
```

Then update `run.py` to accept `--use-ai` flag:
```bash
python -m generator.ai.run --input-dir input --output-dir output --use-ai
```

### AI vs Template Comparison

| Feature | Template-Based | AI-Powered |
|---------|----------------|------------|
| **Speed** | Very Fast (<1s) | Slower (5-10s per service) |
| **Cost** | Free | ~$0.01-0.10 per service |
| **Consistency** | Identical output | Varies slightly |
| **Intelligence** | Fixed patterns | Context-aware |
| **Dependencies** | Python only | OpenAI API, ML libraries |
| **Customization** | Edit templates | Prompt engineering |
| **Best For** | Standard migrations | Complex, unique patterns |

### When to Use AI

✅ **Use AI-powered generation when:**
- TIBCO processes have complex, unique business logic
- You need intelligent mapping of custom activities
- Processes use uncommon patterns
- You want to leverage historical migration knowledge

❌ **Use template-based generation when:**
- Processes follow standard patterns
- Speed is critical
- You want predictable, consistent output
- No OpenAI API access or budget constraints

### RAG Vector Database Details

**Technology:** FAISS (Facebook AI Similarity Search)
- **Type:** In-memory vector database
- **Dimensions:** 384 (sentence-transformers model: `all-MiniLM-L6-v2`)
- **Purpose:** Store TIBCO activity embeddings for similarity search
- **Use Case:** Find similar activities across multiple BW processes

**How It Works:**
1. Parse TIBCO `.process` files and extract activities
2. Convert activity metadata to text representations
3. Generate embeddings using sentence-transformers
4. Store in FAISS index for fast similarity search
5. Query during code generation to find similar patterns

**Example:**
```python
kb = ProcessKnowledgeBase()
kb.index_process_activities("LoanApp.process")
kb.index_process_activities("CreditCheck.process")

# Find similar SQL activities
results = kb.query_similar_activities(
    "SQL query with JOIN and WHERE clause",
    k=3
)

for result in results:
    print(f"Activity: {result['name']}")
    print(f"Similarity: {result['similarity_score']}")
```

### Cost Estimation (AI Mode)

**OpenAI API Costs (GPT-4):**
- Input: ~$0.03 per 1K tokens
- Output: ~$0.06 per 1K tokens
- Average per service: ~2K tokens = **$0.12**

**For 10 BW processes:** ~$1.20  
**For 100 BW processes:** ~$12.00

**Template mode:** $0 (no API calls)

### Migration Path: Template → AI

You don't need to rewrite everything! The framework supports **hybrid mode**:

1. **Phase 1:** Use templates for standard services (90% of processes)
2. **Phase 2:** Enable AI only for complex processes with `--use-ai` flag
3. **Phase 3:** Gradually enhance with LLM where templates fall short

**No breaking changes** - templates remain as fallback!

---

## Hexagonal Architecture Support

The framework now supports **two architectural patterns** for generating Spring Boot services:

1. **Layered Architecture** (Default) - Traditional controller → service → repository structure
2. **Hexagonal Architecture** (New) - Ports & Adapters pattern with domain-driven design

### Architecture Comparison

| Aspect | Layered Architecture | Hexagonal Architecture |
|--------|---------------------|------------------------|
| **Structure** | Controller → Service → Repository | Domain (Ports) ← Adapters |
| **Dependencies** | Top-down (Controller depends on Service) | Inward (Adapters depend on Domain) |
| **Domain Purity** | Domain mixed with framework code | Domain has ZERO framework dependencies |
| **Testability** | Requires mocking Spring components | Pure unit tests without Spring |
| **Technology Coupling** | Tight coupling to Spring | Loose coupling via interfaces |
| **Best For** | Standard CRUD services | Complex business logic, DDD |
| **Generated Projects** | Separate REST and SOAP projects | Single project with multiple adapters |

### Hexagonal Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Hexagonal Architecture                         │
│                    (Ports & Adapters)                            │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │    REST Adapter      │
                    │   (Controller)       │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │   SOAP Adapter       │
                    │   (Endpoint)         │
                    └──────────┬───────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         │        INPUT PORTS (Interfaces)           │
         │     ┌───────────────▼───────────────┐     │
         │     │   LoanApplicationUseCase      │     │
         │     │   (Interface)                 │     │
         │     └───────────────┬───────────────┘     │
         │                     │                     │
         │                     │                     │
         │        ┌────────────▼────────────┐        │
         │        │    DOMAIN LAYER         │        │
         │        │  (Pure Business Logic)  │        │
         │        │                         │        │
         │        │ • LoanApplication       │        │
         │        │ • ApplicantInfo         │        │
         │        │ • CreditScore           │        │
         │        │ • LoanStatus            │        │
         │        │                         │        │
         │        │ LoanApplicationService  │        │
         │        │ (implements UseCase)    │        │
         │        └────────────┬────────────┘        │
         │                     │                     │
         │        OUTPUT PORTS (Interfaces)          │
         │     ┌───────────────┼───────────────┐     │
         │     │ • LoanRepository              │     │
         │     │ • CreditScoreGateway          │     │
         │     │ • NotificationGateway         │     │
         │     └───────────────┬───────────────┘     │
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         │        OUTPUT ADAPTERS                    │
         │                     │                     │
    ┌────▼─────┐     ┌────────▼────────┐     ┌──────▼──────┐
    │   JPA    │     │  HTTP Gateway   │     │     JMS     │
    │ Adapter  │     │    (WebClient)  │     │   Adapter   │
    │(Database)│     │(External APIs)  │     │(Messaging)  │
    └──────────┘     └─────────────────┘     └─────────────┘
```

### Key Principles

**1. Domain Independence:**
- Domain models have NO Spring annotations
- Pure Java POJOs representing business concepts
- No framework dependencies (@Entity, @Component, etc.)

**2. Dependency Inversion:**
- Domain defines interfaces (ports)
- Adapters implement those interfaces
- Dependencies point INWARD toward domain

**3. Adapter Flexibility:**
- Multiple input adapters (REST, SOAP, CLI) can use same domain
- Output adapters (JPA, MongoDB, external APIs) are swappable
- Change technology without touching domain logic

### Generated Structure (Hexagonal)

```
output/hexagonal/
│
├── pom.xml                          # Conditional dependencies
│   ├─ Core: Spring Boot, Spring Context
│   ├─ If REST: spring-boot-starter-web
│   ├─ If SOAP: spring-boot-starter-web-services
│   ├─ Data: spring-boot-starter-data-jpa
│   └─ Messaging: spring-boot-starter-artemis
│
├── src/main/java/com/example/tibco_migration/
│   │
│   ├── HexagonalServiceApplication.java     # @SpringBootApplication
│   │
│   ├── domain/                              # PURE DOMAIN (No framework deps)
│   │   ├── model/
│   │   │   ├── LoanApplication.java         # Pure POJO
│   │   │   ├── ApplicantInfo.java
│   │   │   ├── CreditScore.java
│   │   │   └── LoanStatus.java (enum)
│   │   │
│   │   ├── port/
│   │   │   ├── in/                          # INPUT PORTS
│   │   │   │   └── LoanApplicationUseCase.java  # Interface
│   │   │   │
│   │   │   └── out/                         # OUTPUT PORTS
│   │   │       ├── LoanRepository.java      # Interface (not Spring!)
│   │   │       ├── CreditScoreGateway.java  # Interface
│   │   │       └── NotificationGateway.java # Interface
│   │   │
│   │   └── service/
│   │       └── LoanApplicationService.java  # implements UseCase
│   │           └── Pure business logic
│   │
│   ├── adapter/                             # ADAPTERS (Framework-specific)
│   │   │
│   │   ├── in/                              # INPUT ADAPTERS
│   │   │   ├── rest/                        # REST Adapter (if enabled)
│   │   │   │   ├── controller/
│   │   │   │   │   └── LoanController.java  # @RestController
│   │   │   │   ├── dto/
│   │   │   │   │   ├── LoanRequestDto.java
│   │   │   │   │   └── LoanResponseDto.java
│   │   │   │   └── mapper/
│   │   │   │       └── LoanDtoMapper.java   # DTO ↔ Domain
│   │   │   │
│   │   │   └── soap/                        # SOAP Adapter (if enabled)
│   │   │       ├── endpoint/
│   │   │       │   └── LoanEndpoint.java    # @Endpoint
│   │   │       ├── dto/
│   │   │       │   ├── LoanSoapRequest.java # JAXB annotated
│   │   │       │   └── LoanSoapResponse.java
│   │   │       ├── mapper/
│   │   │       │   └── LoanSoapMapper.java
│   │   │       └── config/
│   │   │           └── WebServiceConfig.java
│   │   │
│   │   └── out/                             # OUTPUT ADAPTERS
│   │       ├── persistence/                 # JPA Adapter
│   │       │   ├── LoanJpaRepository.java   # extends JpaRepository
│   │       │   ├── LoanEntity.java          # @Entity (in adapter!)
│   │       │   └── LoanPersistenceAdapter.java # implements LoanRepository
│   │       │
│   │       ├── http/                        # HTTP Gateway Adapter
│   │       │   └── CreditScoreHttpGateway.java # implements Gateway
│   │       │
│   │       └── jms/                         # JMS Adapter
│   │           └── NotificationJmsAdapter.java # implements Gateway
│   │
│   └── config/
│       ├── AdapterConfig.java               # Bean configuration
│       └── WebClientConfig.java
│
└── src/main/resources/
    ├── application.yml
    └── xsd/
        └── loan.xsd
```

### Usage Examples

#### Generate Hexagonal Architecture (Combined REST + SOAP)

```bash
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output \
  --architecture hexagonal \
  --service-type combined
```

**Output:**
- Single Spring Boot project with both REST and SOAP adapters
- Shared domain logic
- Both adapters call same use case

#### Generate Hexagonal Architecture (REST Only)

```bash
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output \
  --architecture hexagonal \
  --service-type rest
```

**Output:**
- Only REST adapter included in project
- Lighter pom.xml (no Spring-WS dependencies)
- Still follows hexagonal pattern

#### Generate Hexagonal Architecture (SOAP Only)

```bash
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output \
  --architecture hexagonal \
  --service-type soap
```

**Output:**
- Only SOAP adapter included
- No REST controller
- Domain + SOAP endpoint + persistence

#### Generate Traditional Layered Architecture (Default)

```bash
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output
  # --architecture layered (default, can be omitted)
```

**Output:**
- Separate REST and SOAP projects
- Traditional structure (backward compatible)

### Code Examples

#### Domain Model (Pure Java)

```java
// domain/model/LoanApplication.java
package com.example.tibco_migration.domain.model;

// NO Spring annotations! Pure business entity
public class LoanApplication {
    private String loanID;
    private String customerID;
    private double loanAmount;
    private String loanType;
    private int loanTermMonths;
    private ApplicantInfo applicant;
    private LoanStatus status;
    
    // Constructor, getters, setters, business methods
    public void approve(double amount) {
        this.status = LoanStatus.APPROVED;
        this.loanAmount = amount;
    }
    
    public boolean requiresCreditCheck() {
        return loanAmount > 10000;
    }
}
```

#### Input Port (Use Case Interface)

```java
// domain/port/in/LoanApplicationUseCase.java
package com.example.tibco_migration.domain.port.in;

import com.example.tibco_migration.domain.model.LoanApplication;

// Domain-defined interface (NO Spring!)
public interface LoanApplicationUseCase {
    LoanApplication applyForLoan(LoanApplication application);
    LoanApplication getLoanStatus(String loanID);
}
```

#### Domain Service (Business Logic)

```java
// domain/service/LoanApplicationService.java
package com.example.tibco_migration.domain.service;

import com.example.tibco_migration.domain.port.in.LoanApplicationUseCase;
import com.example.tibco_migration.domain.port.out.*;

// Pure business logic - NO @Service annotation!
public class LoanApplicationService implements LoanApplicationUseCase {
    // Dependencies are OUTPUT PORTS (interfaces)
    private final LoanRepository loanRepository;
    private final CreditScoreGateway creditScoreGateway;
    private final NotificationGateway notificationGateway;
    
    // Constructor injection (no @Autowired)
    public LoanApplicationService(
        LoanRepository loanRepository,
        CreditScoreGateway creditScoreGateway,
        NotificationGateway notificationGateway
    ) {
        this.loanRepository = loanRepository;
        this.creditScoreGateway = creditScoreGateway;
        this.notificationGateway = notificationGateway;
    }
    
    @Override
    public LoanApplication applyForLoan(LoanApplication application) {
        // Pure business logic
        if (application.requiresCreditCheck()) {
            CreditScore score = creditScoreGateway.checkCredit(
                application.getCustomerID()
            );
            
            if (score.getScore() > 700) {
                application.approve(application.getLoanAmount());
            } else {
                application.reject("Low credit score");
            }
        }
        
        LoanApplication saved = loanRepository.save(application);
        notificationGateway.sendNotification(saved);
        
        return saved;
    }
}
```

#### Output Port (Repository Interface)

```java
// domain/port/out/LoanRepository.java
package com.example.tibco_migration.domain.port.out;

import com.example.tibco_migration.domain.model.LoanApplication;

// Domain-defined interface (NOT Spring Data JpaRepository!)
public interface LoanRepository {
    LoanApplication save(LoanApplication application);
    LoanApplication findById(String loanID);
}
```

#### REST Adapter (Input)

```java
// adapter/in/rest/controller/LoanController.java
package com.example.tibco_migration.adapter.in.rest.controller;

import org.springframework.web.bind.annotation.*;
import com.example.tibco_migration.domain.port.in.LoanApplicationUseCase;

@RestController  // Spring annotation in ADAPTER only
@RequestMapping("/api/loans")
public class LoanController {
    private final LoanApplicationUseCase loanUseCase;  // Depends on PORT
    private final LoanDtoMapper mapper;
    
    @Autowired
    public LoanController(LoanApplicationUseCase loanUseCase, 
                          LoanDtoMapper mapper) {
        this.loanUseCase = loanUseCase;
        this.mapper = mapper;
    }
    
    @PostMapping("/apply")
    public LoanResponseDto apply(@RequestBody LoanRequestDto dto) {
        // Convert DTO → Domain
        LoanApplication domain = mapper.toDomain(dto);
        
        // Call use case (domain logic)
        LoanApplication result = loanUseCase.applyForLoan(domain);
        
        // Convert Domain → DTO
        return mapper.toDto(result);
    }
}
```

#### JPA Adapter (Output - Persistence)

```java
// adapter/out/persistence/LoanPersistenceAdapter.java
package com.example.tibco_migration.adapter.out.persistence;

import org.springframework.stereotype.Component;
import com.example.tibco_migration.domain.port.out.LoanRepository;
import com.example.tibco_migration.domain.model.LoanApplication;

@Component  // Spring annotation in ADAPTER
public class LoanPersistenceAdapter implements LoanRepository {
    private final LoanJpaRepository jpaRepository;  // Spring Data
    private final LoanEntityMapper mapper;
    
    @Autowired
    public LoanPersistenceAdapter(LoanJpaRepository jpaRepository,
                                   LoanEntityMapper mapper) {
        this.jpaRepository = jpaRepository;
        this.mapper = mapper;
    }
    
    @Override
    public LoanApplication save(LoanApplication application) {
        // Domain → JPA Entity
        LoanEntity entity = mapper.toEntity(application);
        
        // Use Spring Data JPA
        LoanEntity saved = jpaRepository.save(entity);
        
        // JPA Entity → Domain
        return mapper.toDomain(saved);
    }
}

// adapter/out/persistence/LoanJpaRepository.java
@Repository
interface LoanJpaRepository extends JpaRepository<LoanEntity, String> {
    // Spring Data repository
}

// adapter/out/persistence/LoanEntity.java
@Entity
@Table(name = "loans")
class LoanEntity {
    @Id
    private String loanID;
    // JPA annotations in ADAPTER, not domain!
}
```

### Benefits of Hexagonal Architecture

#### 1. Testability
```java
// Test domain service WITHOUT Spring
@Test
void testLoanApproval() {
    // Mock OUTPUT PORTS (simple interfaces)
    LoanRepository mockRepo = mock(LoanRepository.class);
    CreditScoreGateway mockGateway = mock(CreditScoreGateway.class);
    NotificationGateway mockNotifier = mock(NotificationGateway.class);
    
    // Create service (pure Java, no @SpringBootTest)
    LoanApplicationService service = new LoanApplicationService(
        mockRepo, mockGateway, mockNotifier
    );
    
    // Test business logic
    LoanApplication loan = new LoanApplication(...);
    LoanApplication result = service.applyForLoan(loan);
    
    assertEquals(LoanStatus.APPROVED, result.getStatus());
}
```

**Layered architecture requires:**
```java
@SpringBootTest  // Slower, requires full Spring context
@Autowired LoanApplicationService service;
```

#### 2. Technology Swapping
**Change database from JPA to MongoDB:**
- Create `MongoLoanPersistenceAdapter implements LoanRepository`
- Update `AdapterConfig.java` bean
- Domain logic unchanged!

**Change REST to GraphQL:**
- Create `GraphQLAdapter` calling same use case
- Domain logic unchanged!

#### 3. Domain Focus
- Business rules live in domain (not scattered across controllers)
- Domain experts can read pure Java code
- No framework magic obscuring logic

### When to Use Each Architecture

#### Use Layered Architecture When:
- ✅ Simple CRUD operations
- ✅ Standard REST/SOAP services
- ✅ Team familiar with Spring Boot conventions
- ✅ Quick prototypes
- ✅ Small services with minimal business logic

#### Use Hexagonal Architecture When:
- ✅ Complex business logic (DDD approach)
- ✅ Need to support multiple protocols (REST + SOAP + CLI)
- ✅ High testability requirements
- ✅ Technology might change (database, messaging, etc.)
- ✅ Long-term maintainability is critical
- ✅ Domain-driven design principles
- ✅ Team experienced with ports & adapters pattern

### Migration Report (Hexagonal)

```json
{
  "processed_folders": [
    "C:\\...\\input_artifacts\\LoanApp"
  ],
  "generated_files": [
    "C:\\...\\output\\hexagonal\\src\\main\\java\\...\\domain\\model\\LoanApplication.java",
    "C:\\...\\output\\hexagonal\\src\\main\\java\\...\\domain\\port\\in\\LoanApplicationUseCase.java",
    "C:\\...\\output\\hexagonal\\src\\main\\java\\...\\adapter\\in\\rest\\controller\\LoanController.java",
    "C:\\...\\output\\hexagonal\\src\\main\\java\\...\\adapter\\in\\soap\\endpoint\\LoanEndpoint.java"
  ],
  "validation": {
    "C:\\...\\output\\hexagonal": {
      "compiled": true,
      "mvn_available": true
    }
  },
  "archives": [
    "C:\\...\\output\\LoanApp_hexagonal_combined.zip"
  ]
}
```

### Configuration (application.yml)

```yaml
server:
  port: 8080  # Default for REST

spring:
  application:
    name: hexagonal-loan-service
  
  datasource:
    url: jdbc:h2:mem:loandb
    driver-class-name: org.h2.Driver
  
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
  
  artemis:
    mode: embedded
  
  # SOAP configuration (if service-type includes SOAP)
  webservices:
    path: /ws
```

### Build and Run

#### Build Hexagonal Service
```bash
cd output/hexagonal
mvn clean package
```

#### Run Hexagonal Service
```bash
java -jar target/hexagonal-loan-service-0.1.0.jar
```

**Access:**
- REST API: `http://localhost:8080/api/loans/apply`
- SOAP WSDL: `http://localhost:8080/ws/loanApplication.wsdl` (if SOAP enabled)

### Architecture Decision Record (ADR)

**Decision:** Support both Layered and Hexagonal architectures

**Context:**
- Layered architecture is familiar, fast to generate, good for simple services
- Hexagonal architecture provides better separation, testability, and flexibility
- Different teams have different preferences and requirements

**Decision:**
- Keep layered as default (backward compatibility)
- Add hexagonal as optional via `--architecture hexagonal`
- Generate appropriate structure based on flag
- Both architectures support REST, SOAP, or combined modes

**Consequences:**
- ✅ Flexibility for different use cases
- ✅ Backward compatible (existing users unaffected)
- ✅ Educational value (teams can learn hexagonal)
- ⚠️ Two code paths to maintain
- ⚠️ Slightly larger codebase

---

## Best Practices

### 1. Input Preparation
- Organize BW processes into separate folders
- Include all dependent XSD files
- Ensure `.process` files are well-formed XML

### 2. Review Generated Code
- Generated code is a **starting point**, not production-ready
- Review and enhance business logic
- Add error handling and validation
- Implement security (authentication, authorization)

### 3. Testing
- Write unit tests for service layer
- Integration tests for endpoints
- Test database operations
- Verify JMS messaging

### 4. Production Deployment
- Use external database (not H2)
- Configure external JMS broker
- Set up proper logging
- Add monitoring (Actuator)
- Implement health checks

### 5. Performance Tuning
- Configure connection pools
- Optimize JPA queries
- Add caching (Spring Cache)
- Use async processing where appropriate

---

## Appendix

### File Locations

| Component | Path |
|-----------|------|
| Main orchestrator | `generator/generator/ai/leader.py` |
| Process parser | `generator/generator/process_parser.py` |
| XSD parser | `generator/generator/xsd_parser.py` |
| REST agent | `generator/generator/ai/service_agents.py` (RestServiceAgent) |
| SOAP agent | `generator/generator/ai/service_agents.py` (SoapServiceAgent) |
| Migration runner | `generator/generator/ai/run.py` |
| Templates | `generator/generator/templates.py` |

### Command Reference

```bash
# Run migration
python -m generator.ai.run --input-dir <input> --output-dir <output>

# Build REST service
cd output/rest && mvn clean package

# Build SOAP service
cd output/soap && mvn clean package

# Run REST service
cd output/rest && mvn spring-boot:run

# Run SOAP service
cd output/soap && mvn spring-boot:run

# Package as ZIP
# (Automatically done during migration)
```

### URLs After Deployment

| Service | URL |
|---------|-----|
| REST API | http://localhost:8080 |
| REST Swagger (if added) | http://localhost:8080/swagger-ui.html |
| SOAP WSDL | http://localhost:8081/ws/loanApplication.wsdl |
| H2 Console (REST) | http://localhost:8080/h2-console |
| H2 Console (SOAP) | http://localhost:8081/h2-console |

---

## API Gateway (Spring Cloud Gateway)

The framework can generate a **Spring Cloud Gateway** to provide a single entry point for all microservices (REST, SOAP, layered, hexagonal).

### Overview

Spring Cloud Gateway acts as a reverse proxy that routes requests to backend services with advanced features:

- **Unified Entry Point**: Single endpoint at `http://localhost:8080`
- **Dynamic Routing**: Path-based and header-based routing
- **Circuit Breaker**: Fault tolerance with Resilience4j
- **Rate Limiting**: Prevent API abuse (Redis-based)
- **CORS**: Cross-origin resource sharing configuration
- **Load Balancing**: Distribute traffic across service instances
- **Monitoring**: Actuator endpoints for health checks and metrics
- **Logging**: Request/response tracking with custom filters

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      External Clients                         │
│         (Web Apps, Mobile Apps, Third-party Systems)          │
└──────────────┬───────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────┐
│           API Gateway (Spring Cloud Gateway)                  │
│                    Port: 8080                                 │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Features:                                              │  │
│  │ • Path-based routing (/api/**, /ws/**)                │  │
│  │ • Circuit breaker (Resilience4j)                      │  │
│  │ • Rate limiting (Redis)                               │  │
│  │ • CORS configuration                                  │  │
│  │ • Request/response filtering                          │  │
│  │ • Monitoring (Actuator)                               │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────┬─────────────┬─────────────┬────────────────────────┘
           │             │             │
           ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐
│  REST Service│ │  SOAP Service│ │ Hexagonal Service        │
│  (Layered)   │ │  (Layered)   │ │ (Ports & Adapters)       │
│  Port: 8081  │ │  Port: 8082  │ │ Port: 8083               │
│              │ │              │ │                          │
│ /api/loan/** │ │ /ws/loan/**  │ │ /api/process/** (REST)   │
│              │ │              │ │ /ws/process/** (SOAP)    │
└──────────────┘ └──────────────┘ └──────────────────────────┘
```

### Generated Components

#### 1. Gateway Application (`ApiGatewayApplication.java`)
```java
@SpringBootApplication
public class ApiGatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(ApiGatewayApplication.class, args);
    }
}
```

#### 2. Route Configuration (`RouteConfig.java`)
Automatically configures routes for all generated services:

```java
@Configuration
public class RouteConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            // REST service route
            .route("loan_rest_route", r -> r
                .path("/api/loanapplication/**")
                .filters(f -> f
                    .stripPrefix(1)
                    .addRequestHeader("X-Gateway-Route", "loan_rest")
                    .circuitBreaker(c -> c
                        .setName("loan_cb")
                        .setFallbackUri("forward:/fallback/loan"))
                    .retry(config -> config.setRetries(3)))
                .uri("http://localhost:8081"))
            
            // SOAP service route
            .route("loan_soap_route", r -> r
                .path("/ws/loanapplication/**")
                .filters(f -> f
                    .stripPrefix(1)
                    .addRequestHeader("X-Gateway-Route", "loan_soap")
                    .circuitBreaker(c -> c
                        .setName("loan_soap_cb")
                        .setFallbackUri("forward:/fallback/loan")))
                .uri("http://localhost:8081"))
            .build();
    }
}
```

#### 3. CORS Configuration (`CorsConfig.java`)
```java
@Configuration
public class CorsConfig {
    @Bean
    public CorsWebFilter corsWebFilter() {
        CorsConfiguration corsConfig = new CorsConfiguration();
        corsConfig.setAllowedOriginPatterns(List.of("*"));
        corsConfig.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"));
        corsConfig.setAllowedHeaders(Arrays.asList("Authorization", "Content-Type", "X-User-Id"));
        corsConfig.setAllowCredentials(true);
        corsConfig.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", corsConfig);
        return new CorsWebFilter(source);
    }
}
```

#### 4. Gateway Configuration (`GatewayConfig.java`)
```java
@Configuration
public class GatewayConfig {
    // IP-based rate limiting
    @Bean
    public KeyResolver ipKeyResolver() {
        return exchange -> Mono.just(
            exchange.getRequest()
                .getRemoteAddress()
                .getAddress()
                .getHostAddress()
        );
    }
    
    // User-based rate limiting
    @Bean
    public KeyResolver userKeyResolver() {
        return exchange -> Mono.justOrEmpty(
            exchange.getRequest()
                .getHeaders()
                .getFirst("X-User-Id")
        ).defaultIfEmpty("anonymous");
    }
}
```

#### 5. Custom Logging Filter (`LoggingGatewayFilterFactory.java`)
```java
@Component
public class LoggingGatewayFilterFactory 
    extends AbstractGatewayFilterFactory<LoggingGatewayFilterFactory.Config> {
    
    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            logger.info("Pre-filter: {} {}", 
                exchange.getRequest().getMethod(),
                exchange.getRequest().getURI());
            
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                logger.info("Post-filter: Response status: {}", 
                    exchange.getResponse().getStatusCode());
            }));
        };
    }
}
```

### Configuration (`application.yml`)

```yaml
spring:
  application:
    name: api-gateway
  
  cloud:
    gateway:
      globalcors:
        corsConfigurations:
          '[/**]':
            allowedOrigins: "*"
            allowedMethods:
              - GET
              - POST
              - PUT
              - DELETE
              - OPTIONS
            allowedHeaders: "*"
      
      default-filters:
        - DedupeResponseHeader=Access-Control-Allow-Credentials Access-Control-Allow-Origin
      
      httpclient:
        connect-timeout: 5000
        response-timeout: 30s
  
  redis:
    host: localhost
    port: 6379

server:
  port: 8080

management:
  endpoints:
    web:
      exposure:
        include: health,info,gateway,metrics

resilience4j:
  circuitbreaker:
    configs:
      default:
        registerHealthIndicator: true
        slidingWindowSize: 10
        minimumNumberOfCalls: 5
        failureRateThreshold: 50
        waitDurationInOpenState: 10s

logging:
  level:
    org.springframework.cloud.gateway: INFO
```

### Usage

#### Generate with Gateway

```bash
# Layered architecture with gateway
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output \
  --gateway

# Hexagonal architecture with gateway
python -m generator.ai.run \
  --input-dir input_artifacts \
  --output-dir output \
  --architecture hexagonal \
  --service-type combined \
  --gateway
```

#### Run Gateway and Services

```bash
# 1. Start backend service(s)
cd output/hexagonal
mvn spring-boot:run  # Runs on port 8081

# 2. Start API Gateway (in new terminal)
cd output/api-gateway
mvn spring-boot:run  # Runs on port 8080

# 3. Access via gateway
curl http://localhost:8080/api/loanapplication/loans/apply

# 4. Check gateway routes
curl http://localhost:8080/actuator/gateway/routes

# 5. Check health
curl http://localhost:8080/actuator/health
```

### Route Patterns

The gateway automatically configures routes based on generated services:

| Service Type | Pattern | Example | Backend |
|-------------|---------|---------|---------|
| REST (Layered) | `/api/{service}/**` | `/api/loanapplication/**` | `http://localhost:8081` |
| SOAP (Layered) | `/ws/{service}/**` | `/ws/loanapplication/**` | `http://localhost:8082` |
| Hexagonal (REST) | `/api/{service}/**` | `/api/loanprocess/**` | `http://localhost:8083` |
| Hexagonal (SOAP) | `/ws/{service}/**` | `/ws/loanprocess/**` | `http://localhost:8083` |
| Hexagonal (Combined) | Both patterns | Both REST & SOAP | `http://localhost:8083` |

### Features in Detail

#### Circuit Breaker

Each route is protected with a circuit breaker:
- **Sliding Window Size**: 10 calls
- **Failure Rate Threshold**: 50%
- **Wait Duration in Open State**: 10 seconds
- **Half-Open Permitted Calls**: 3
- **Fallback**: Forwards to `/fallback/{service}`

```java
.circuitBreaker(c -> c
    .setName("service_cb")
    .setFallbackUri("forward:/fallback/service"))
```

#### Rate Limiting

Configure per-route rate limiting:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: loan_service
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10  # requests per second
                redis-rate-limiter.burstCapacity: 20  # max burst
                key-resolver: "#{@ipKeyResolver}"
```

#### Retry Mechanism

Failed requests are automatically retried:
- **Default Retries**: 3 attempts
- **Retry on**: 5xx errors, connection timeouts
- **Backoff**: None (configurable)

```java
.retry(config -> config.setRetries(3))
```

### Monitoring Endpoints

| Endpoint | Description |
|----------|-------------|
| `/actuator/health` | Gateway health status |
| `/actuator/gateway/routes` | List all configured routes |
| `/actuator/metrics` | Gateway metrics |
| `/actuator/gateway/routes/{id}` | Specific route details |
| `/actuator/gateway/refresh` | Refresh routes |

### Production Considerations

1. **CORS**: Restrict `allowedOrigins` to specific domains
   ```java
   corsConfig.setAllowedOrigins(Arrays.asList(
       "https://app.example.com",
       "https://admin.example.com"
   ));
   ```

2. **Rate Limiting**: Enable Redis and configure appropriate limits
   ```yaml
   spring:
     redis:
       host: redis-prod.example.com
       port: 6379
       password: ${REDIS_PASSWORD}
   ```

3. **SSL/TLS**: Configure HTTPS
   ```yaml
   server:
     port: 8443
     ssl:
       enabled: true
       key-store: classpath:keystore.p12
       key-store-password: ${KEYSTORE_PASSWORD}
       key-store-type: PKCS12
   ```

4. **Service Discovery**: Integrate with Eureka/Consul
   ```yaml
   spring:
     cloud:
       gateway:
         discovery:
           locator:
             enabled: true
             lower-case-service-id: true
   ```

5. **Authentication**: Add Spring Security filter
   ```java
   .filters(f -> f
       .filter(authenticationFilter)
       .stripPrefix(1))
   ```

### Troubleshooting

#### Route Not Found (404)
```bash
# Check route configuration
curl http://localhost:8080/actuator/gateway/routes

# Verify backend service is running
curl http://localhost:8081/actuator/health

# Check gateway logs
tail -f logs/api-gateway.log
```

#### Circuit Breaker Open
```bash
# Check circuit breaker status
curl http://localhost:8080/actuator/health

# View metrics
curl http://localhost:8080/actuator/metrics/resilience4j.circuitbreaker.state

# Verify backend service health
curl http://localhost:8081/actuator/health
```

#### CORS Errors
```bash
# Check CORS configuration in browser console
# Verify preflight requests (OPTIONS) are handled

# Test CORS manually
curl -X OPTIONS http://localhost:8080/api/loan/apply \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

#### Rate Limiting Issues
```bash
# Verify Redis is running
redis-cli ping  # Should return PONG

# Check Redis connection in gateway logs
# Adjust rate limits in application.yml
```

### Dependencies (`pom.xml`)

```xml
<dependencies>
    <!-- Spring Cloud Gateway -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-gateway</artifactId>
    </dependency>
    
    <!-- Actuator -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    
    <!-- Circuit Breaker -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-circuitbreaker-reactor-resilience4j</artifactId>
    </dependency>
    
    <!-- Redis (Rate Limiting) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis-reactive</artifactId>
    </dependency>
</dependencies>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>2022.0.4</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Architecture Decision Record (ADR)

**Decision**: Use Spring Cloud Gateway for API Gateway

**Context**: Need unified entry point for multiple microservices with advanced routing capabilities

**Alternatives Considered**:
1. **Netflix Zuul**: Deprecated in favor of Spring Cloud Gateway
2. **Kong Gateway**: Requires separate infrastructure, not JVM-based
3. **NGINX**: Limited Spring integration, requires Lua scripting

**Rationale**:
- **Native Spring Integration**: Seamless integration with Spring Boot ecosystem
- **Reactive**: Built on Spring WebFlux for non-blocking I/O
- **Rich Feature Set**: Circuit breaker, rate limiting, filters out-of-the-box
- **Easy Configuration**: Java-based or YAML configuration
- **Actuator Integration**: Built-in monitoring and health checks
- **Active Development**: Actively maintained by Spring team

**Consequences**:
- ✅ Unified routing and cross-cutting concerns
- ✅ Better performance with reactive model
- ✅ Easy to extend with custom filters
- ⚠️ Requires Redis for rate limiting (optional)
- ⚠️ Learning curve for WebFlux (reactive programming)

---

## Support & Contributions

For issues or enhancements:
1. Review this documentation
2. Check troubleshooting section
3. Examine generated code and logs
4. Modify templates in `service_agents.py` for custom generation

---

**Document Version:** 1.0  
**Last Updated:** October 30, 2025  
**Project:** TIBCO BusinessWorks to Spring Boot Migration Framework
