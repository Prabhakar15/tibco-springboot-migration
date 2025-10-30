# TIBCO Migration - SOAP Service

This is a Spring Boot SOAP web service implementation migrated from TIBCO BusinessWorks. It provides loan application processing via SOAP/WSDL.

## Architecture

- **Framework**: Spring Boot 3.2.0 with Spring Web Services
- **SOAP Version**: SOAP 1.1 / 1.2
- **JAXB**: For XML marshalling/unmarshalling
- **Database**: H2 (in-memory) / Oracle (configurable)
- **JMS**: Embedded Artemis
- **Build Tool**: Maven

## Project Structure

```
soap/
├── src/main/java/com/example/tibco_migration/
│   ├── SoapServiceApplication.java          # Main Spring Boot application
│   ├── config/
│   │   ├── WebServiceConfig.java           # SOAP/WSDL configuration
│   │   └── WebClientConfig.java            # WebClient for REST calls
│   ├── endpoint/
│   │   └── LoanApplicationEndpoint.java    # SOAP endpoint (@Endpoint)
│   ├── dto/
│   │   ├── LoanApplicationRequest.java     # JAXB request DTO
│   │   └── LoanApplicationResponse.java    # JAXB response DTO
│   ├── service/
│   │   └── LoanApplicationService.java     # Business logic
│   ├── repository/
│   │   └── LoanRepository.java             # JPA repository
│   └── entity/
│       └── LoanEntity.java                 # JPA entity
└── src/main/resources/
    ├── application.yml                      # Configuration
    └── xsd/
        ├── loan_request.xsd                 # Request/Response XSD schema
        ├── creditscore_request.xsd
        ├── creditscore_response.xsd
        └── bindings.xjb                     # JAXB bindings

```

## Key Features

1. **SOAP Web Service**
   - Exposes loan application service via SOAP
   - Auto-generated WSDL available at: `http://localhost:8081/ws/loanApplication.wsdl`
   - Spring-WS with JAXB marshalling

2. **Database Integration**
   - JPA/Hibernate for database operations
   - H2 in-memory database (default)
   - Configurable for Oracle/other databases

3. **JMS Messaging**
   - Embedded Apache Artemis
   - Publishes loan status to queue

4. **External Service Call**
   - WebClient for credit score service integration

## Building and Running

### Prerequisites
- Java 17 or higher
- Maven 3.6+

### Build
```bash
cd soap
mvn clean package
```

### Run
```bash
mvn spring-boot:run
```

Or run the JAR:
```bash
java -jar target/tibco-migration-soap-0.1.0.jar
```

The service will start on port **8081**.

## WSDL Access

Once running, access the WSDL at:
```
http://localhost:8081/ws/loanApplication.wsdl
```

## Testing with SOAP UI or curl

### Sample SOAP Request

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

### Using curl

```bash
curl -X POST http://localhost:8081/ws \
  -H "Content-Type: text/xml" \
  -H "SOAPAction: \"\"" \
  -d @request.xml
```

Where `request.xml` contains the SOAP request above.

## Configuration

Key configuration in `application.yml`:

```yaml
server:
  port: 8081                    # SOAP service port

spring:
  datasource:
    url: jdbc:h2:mem:loandb     # Database URL
  
creditscore:
  service:
    url: http://localhost:8082/creditscore  # Credit score service
```

### Database Configuration

To use Oracle instead of H2:

1. Uncomment Oracle dependency in `pom.xml`
2. Update `application.yml`:
```yaml
spring:
  datasource:
    url: jdbc:oracle:thin:@localhost:1521:XE
    username: your_username
    password: your_password
    driver-class-name: oracle.jdbc.OracleDriver
```

## Endpoints

| Operation | SOAP Action | Description |
|-----------|-------------|-------------|
| applyForLoan | LoanApplicationRequest | Submit loan application |

## Business Logic Flow

1. Receive SOAP request with loan application details
2. Save loan application to database
3. Call external credit score service (REST)
4. Evaluate credit score and approve/reject loan
5. Update database with decision
6. Send status message to JMS queue
7. Return SOAP response

## Logging

Enable detailed SOAP logging:
```yaml
logging:
  level:
    org.springframework.ws: DEBUG
```

## H2 Console

Access the H2 database console at:
```
http://localhost:8081/h2-console
```
- JDBC URL: `jdbc:h2:mem:loandb`
- Username: `sa`
- Password: (empty)

## Notes

- This is a contract-first SOAP service (XSD-driven)
- JAXB classes can be auto-generated from XSD using the maven plugin
- The service is stateless and suitable for horizontal scaling
- For production, configure external database and JMS broker
