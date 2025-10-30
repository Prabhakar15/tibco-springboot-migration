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
