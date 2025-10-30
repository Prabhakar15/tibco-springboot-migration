"""Hexagonal Architecture (Ports & Adapters) service generators.

This module generates Spring Boot services using Hexagonal Architecture pattern,
separating domain logic from infrastructure concerns through ports and adapters.
"""
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class HexagonalServiceAgent:
    """Generate services using Hexagonal/Ports & Adapters architecture pattern.
    
    Supports three modes:
    - 'rest': REST adapter only
    - 'soap': SOAP adapter only  
    - 'combined': Both REST and SOAP adapters sharing same domain
    """

    def __init__(self, process_context: Any, service_type: str = 'combined'):
        self.ctx = process_context
        self.service_type = service_type  # 'rest', 'soap', or 'combined'

    def generate(self) -> Dict[str, str]:
        """Generate complete hexagonal architecture project."""
        files: Dict[str, str] = {}
        # Create hexagonal subfolder to avoid cluttering output root
        out = Path(self.ctx.output_folder) / 'hexagonal'
        pkg = self.ctx.package_root + '.hexagonal'

        # Domain layer (core business logic - no dependencies)
        files.update(self._generate_domain_model(out, pkg))
        files.update(self._generate_use_case_ports(out, pkg))
        files.update(self._generate_domain_service(out, pkg))
        files.update(self._generate_output_ports(out, pkg))

        # Input adapters (based on service_type)
        if self.service_type in ['rest', 'combined']:
            files.update(self._generate_rest_adapter(out, pkg))
        
        if self.service_type in ['soap', 'combined']:
            files.update(self._generate_soap_adapter(out, pkg))

        # Output adapters (infrastructure)
        files.update(self._generate_persistence_adapter(out, pkg))
        files.update(self._generate_http_gateway_adapter(out, pkg))
        files.update(self._generate_jms_adapter(out, pkg))

        # Configuration
        files.update(self._generate_application_class(out, pkg))
        files.update(self._generate_adapter_config(out, pkg))
        files.update(self._generate_application_yml(out, pkg))
        files.update(self._generate_pom(out))
        files.update(self._generate_readme(out))

        logger.info(f"Generated Hexagonal architecture service ({self.service_type}) for {out}")
        return files

    # ==================== DOMAIN LAYER ====================
    
    def _generate_domain_model(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate domain model (pure business entities)."""
        files = {}
        model_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'domain' / 'model'
        model_dir.mkdir(parents=True, exist_ok=True)

        # LoanApplication domain entity
        files[str(model_dir / 'LoanApplication.java')] = f"""package {pkg}.domain.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Domain model for Loan Application.
 * Pure business entity with no framework dependencies.
 */
public class LoanApplication {{
    
    private String id;
    private ApplicantInfo applicant;
    private BigDecimal amount;
    private Integer termMonths;
    private CreditScore creditScore;
    private LoanStatus status;
    private LocalDateTime appliedAt;
    private LocalDateTime processedAt;

    // Constructor
    public LoanApplication() {{
        this.appliedAt = LocalDateTime.now();
        this.status = LoanStatus.PENDING;
    }}

    // Business methods
    public void approve() {{
        if (this.creditScore == null || this.creditScore.getScore() < 600) {{
            throw new IllegalStateException("Cannot approve loan with credit score < 600");
        }}
        this.status = LoanStatus.APPROVED;
        this.processedAt = LocalDateTime.now();
    }}

    public void reject(String reason) {{
        this.status = LoanStatus.REJECTED;
        this.processedAt = LocalDateTime.now();
    }}

    public boolean isApproved() {{
        return LoanStatus.APPROVED.equals(this.status);
    }}

    // Getters and setters
    public String getId() {{ return id; }}
    public void setId(String id) {{ this.id = id; }}

    public ApplicantInfo getApplicant() {{ return applicant; }}
    public void setApplicant(ApplicantInfo applicant) {{ this.applicant = applicant; }}

    public BigDecimal getAmount() {{ return amount; }}
    public void setAmount(BigDecimal amount) {{ this.amount = amount; }}

    public Integer getTermMonths() {{ return termMonths; }}
    public void setTermMonths(Integer termMonths) {{ this.termMonths = termMonths; }}

    public CreditScore getCreditScore() {{ return creditScore; }}
    public void setCreditScore(CreditScore creditScore) {{ this.creditScore = creditScore; }}

    public LoanStatus getStatus() {{ return status; }}
    public void setStatus(LoanStatus status) {{ this.status = status; }}

    public LocalDateTime getAppliedAt() {{ return appliedAt; }}
    public void setAppliedAt(LocalDateTime appliedAt) {{ this.appliedAt = appliedAt; }}

    public LocalDateTime getProcessedAt() {{ return processedAt; }}
    public void setProcessedAt(LocalDateTime processedAt) {{ this.processedAt = processedAt; }}
}}
"""

        # ApplicantInfo value object
        files[str(model_dir / 'ApplicantInfo.java')] = f"""package {pkg}.domain.model;

public class ApplicantInfo {{
    
    private String firstName;
    private String lastName;
    private String ssn;
    private String email;
    private String phone;

    // Getters and setters
    public String getFirstName() {{ return firstName; }}
    public void setFirstName(String firstName) {{ this.firstName = firstName; }}

    public String getLastName() {{ return lastName; }}
    public void setLastName(String lastName) {{ this.lastName = lastName; }}

    public String getSsn() {{ return ssn; }}
    public void setSsn(String ssn) {{ this.ssn = ssn; }}

    public String getEmail() {{ return email; }}
    public void setEmail(String email) {{ this.email = email; }}

    public String getPhone() {{ return phone; }}
    public void setPhone(String phone) {{ this.phone = phone; }}
    
    public String getFullName() {{
        return firstName + " " + lastName;
    }}
}}
"""

        # CreditScore value object
        files[str(model_dir / 'CreditScore.java')] = f"""package {pkg}.domain.model;

public class CreditScore {{
    
    private int score;
    private String rating;

    public CreditScore(int score) {{
        this.score = score;
        this.rating = calculateRating(score);
    }}

    private String calculateRating(int score) {{
        if (score >= 750) return "EXCELLENT";
        if (score >= 700) return "GOOD";
        if (score >= 650) return "FAIR";
        if (score >= 600) return "POOR";
        return "VERY_POOR";
    }}

    public int getScore() {{ return score; }}
    public String getRating() {{ return rating; }}
}}
"""

        # LoanStatus enum
        files[str(model_dir / 'LoanStatus.java')] = f"""package {pkg}.domain.model;

public enum LoanStatus {{
    PENDING,
    APPROVED,
    REJECTED
}}
"""

        return files

    def _generate_use_case_ports(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate input ports (use case interfaces)."""
        files = {}
        port_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'domain' / 'port' / 'input'
        port_dir.mkdir(parents=True, exist_ok=True)

        files[str(port_dir / 'LoanApplicationUseCase.java')] = f"""package {pkg}.domain.port.input;

import {pkg}.domain.model.LoanApplication;

/**
 * Input port for loan application use cases.
 * This is the interface that adapters (REST, SOAP) will call.
 */
public interface LoanApplicationUseCase {{
    
    /**
     * Apply for a new loan.
     * @param application The loan application details
     * @return The processed loan application with ID and credit score
     */
    LoanApplication applyForLoan(LoanApplication application);
    
    /**
     * Retrieve a loan application by ID.
     * @param loanId The loan ID
     * @return The loan application if found
     */
    LoanApplication getLoanById(String loanId);
}}
"""

        return files

    def _generate_domain_service(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate domain service (business logic implementation)."""
        files = {}
        service_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'domain' / 'service'
        service_dir.mkdir(parents=True, exist_ok=True)

        files[str(service_dir / 'LoanApplicationService.java')] = f"""package {pkg}.domain.service;

import {pkg}.domain.model.LoanApplication;
import {pkg}.domain.model.CreditScore;
import {pkg}.domain.port.input.LoanApplicationUseCase;
import {pkg}.domain.port.output.LoanRepository;
import {pkg}.domain.port.output.CreditScoreGateway;
import {pkg}.domain.port.output.NotificationGateway;

import java.util.UUID;

/**
 * Core business logic for loan application processing.
 * Implements use case by orchestrating domain model and output ports.
 * 
 * NOTE: This is a PURE domain service with NO framework dependencies.
 * Spring configuration happens in the adapter layer (AdapterConfig).
 */
public class LoanApplicationService implements LoanApplicationUseCase {{
    
    private final LoanRepository loanRepository;
    private final CreditScoreGateway creditScoreGateway;
    private final NotificationGateway notificationGateway;
    
    public LoanApplicationService(
            LoanRepository loanRepository,
            CreditScoreGateway creditScoreGateway,
            NotificationGateway notificationGateway) {{
        this.loanRepository = loanRepository;
        this.creditScoreGateway = creditScoreGateway;
        this.notificationGateway = notificationGateway;
    }}
    
    @Override
    public LoanApplication applyForLoan(LoanApplication application) {{
        // Generate ID
        application.setId(UUID.randomUUID().toString());
        
        // Check credit score via gateway
        CreditScore score = creditScoreGateway.checkCredit(application.getApplicant());
        application.setCreditScore(score);
        
        // Business rule: approve if score >= 600
        if (score.getScore() >= 600) {{
            application.approve();
        }} else {{
            application.reject("Credit score below minimum threshold");
        }}
        
        // Save via repository
        LoanApplication saved = loanRepository.save(application);
        
        // Send notification
        notificationGateway.sendApplicationNotification(saved);
        
        return saved;
    }}
    
    @Override
    public LoanApplication getLoanById(String loanId) {{
        return loanRepository.findById(loanId)
                .orElseThrow(() -> new IllegalArgumentException("Loan not found: " + loanId));
    }}
}}
"""

        return files

    def _generate_output_ports(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate output ports (interfaces for infrastructure)."""
        files = {}
        port_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'domain' / 'port' / 'output'
        port_dir.mkdir(parents=True, exist_ok=True)

        # Repository port
        files[str(port_dir / 'LoanRepository.java')] = f"""package {pkg}.domain.port.output;

import {pkg}.domain.model.LoanApplication;
import java.util.Optional;

/**
 * Output port for loan persistence.
 * Infrastructure adapter will implement this.
 */
public interface LoanRepository {{
    LoanApplication save(LoanApplication loan);
    Optional<LoanApplication> findById(String id);
}}
"""

        # Credit score gateway port
        files[str(port_dir / 'CreditScoreGateway.java')] = f"""package {pkg}.domain.port.output;

import {pkg}.domain.model.ApplicantInfo;
import {pkg}.domain.model.CreditScore;

/**
 * Output port for credit score checking.
 * HTTP client adapter will implement this.
 */
public interface CreditScoreGateway {{
    CreditScore checkCredit(ApplicantInfo applicant);
}}
"""

        # Notification gateway port
        files[str(port_dir / 'NotificationGateway.java')] = f"""package {pkg}.domain.port.output;

import {pkg}.domain.model.LoanApplication;

/**
 * Output port for sending notifications.
 * JMS adapter will implement this.
 */
public interface NotificationGateway {{
    void sendApplicationNotification(LoanApplication loan);
}}
"""

        return files

    # ==================== INPUT ADAPTERS ====================

    def _generate_rest_adapter(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate REST adapter (controller + DTOs)."""
        files = {}
        
        # Controller
        controller_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'adapter' / 'input' / 'rest'
        controller_dir.mkdir(parents=True, exist_ok=True)

        files[str(controller_dir / 'LoanRestController.java')] = f"""package {pkg}.adapter.input.rest;

import {pkg}.domain.port.input.LoanApplicationUseCase;
import {pkg}.domain.model.LoanApplication;
import {pkg}.adapter.input.rest.dto.LoanRequestDto;
import {pkg}.adapter.input.rest.dto.LoanResponseDto;
import {pkg}.adapter.input.rest.mapper.LoanDtoMapper;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

/**
 * REST adapter for loan application use case.
 */
@RestController
@RequestMapping("/api/loans")
public class LoanRestController {{
    
    private final LoanApplicationUseCase loanUseCase;
    
    public LoanRestController(LoanApplicationUseCase loanUseCase) {{
        this.loanUseCase = loanUseCase;
    }}
    
    @PostMapping("/apply")
    public ResponseEntity<LoanResponseDto> applyForLoan(@Valid @RequestBody LoanRequestDto dto) {{
        // Map DTO to domain
        LoanApplication domain = LoanDtoMapper.toDomain(dto);
        
        // Execute use case
        LoanApplication result = loanUseCase.applyForLoan(domain);
        
        // Map domain to DTO
        LoanResponseDto response = LoanDtoMapper.toDto(result);
        
        return ResponseEntity.ok(response);
    }}
    
    @GetMapping("/{{loanId}}")
    public ResponseEntity<LoanResponseDto> getLoan(@PathVariable String loanId) {{
        LoanApplication loan = loanUseCase.getLoanById(loanId);
        return ResponseEntity.ok(LoanDtoMapper.toDto(loan));
    }}
}}
"""

        # DTOs
        dto_dir = controller_dir / 'dto'
        dto_dir.mkdir(exist_ok=True)

        files[str(dto_dir / 'LoanRequestDto.java')] = f"""package {pkg}.adapter.input.rest.dto;

import jakarta.validation.constraints.*;
import java.math.BigDecimal;

public class LoanRequestDto {{
    
    @NotBlank
    private String firstName;
    
    @NotBlank
    private String lastName;
    
    @NotBlank
    private String ssn;
    
    @Email
    private String email;
    
    @Positive
    private BigDecimal amount;
    
    @Min(12)
    @Max(360)
    private Integer termMonths;

    // Getters and setters
    public String getFirstName() {{ return firstName; }}
    public void setFirstName(String firstName) {{ this.firstName = firstName; }}

    public String getLastName() {{ return lastName; }}
    public void setLastName(String lastName) {{ this.lastName = lastName; }}

    public String getSsn() {{ return ssn; }}
    public void setSsn(String ssn) {{ this.ssn = ssn; }}

    public String getEmail() {{ return email; }}
    public void setEmail(String email) {{ this.email = email; }}

    public BigDecimal getAmount() {{ return amount; }}
    public void setAmount(BigDecimal amount) {{ this.amount = amount; }}

    public Integer getTermMonths() {{ return termMonths; }}
    public void setTermMonths(Integer termMonths) {{ this.termMonths = termMonths; }}
}}
"""

        files[str(dto_dir / 'LoanResponseDto.java')] = f"""package {pkg}.adapter.input.rest.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class LoanResponseDto {{
    
    private String loanId;
    private String applicantName;
    private BigDecimal amount;
    private Integer termMonths;
    private Integer creditScore;
    private String status;
    private LocalDateTime appliedAt;
    private LocalDateTime processedAt;

    // Getters and setters
    public String getLoanId() {{ return loanId; }}
    public void setLoanId(String loanId) {{ this.loanId = loanId; }}

    public String getApplicantName() {{ return applicantName; }}
    public void setApplicantName(String applicantName) {{ this.applicantName = applicantName; }}

    public BigDecimal getAmount() {{ return amount; }}
    public void setAmount(BigDecimal amount) {{ this.amount = amount; }}

    public Integer getTermMonths() {{ return termMonths; }}
    public void setTermMonths(Integer termMonths) {{ this.termMonths = termMonths; }}

    public Integer getCreditScore() {{ return creditScore; }}
    public void setCreditScore(Integer creditScore) {{ this.creditScore = creditScore; }}

    public String getStatus() {{ return status; }}
    public void setStatus(String status) {{ this.status = status; }}

    public LocalDateTime getAppliedAt() {{ return appliedAt; }}
    public void setAppliedAt(LocalDateTime appliedAt) {{ this.appliedAt = appliedAt; }}

    public LocalDateTime getProcessedAt() {{ return processedAt; }}
    public void setProcessedAt(LocalDateTime processedAt) {{ this.processedAt = processedAt; }}
}}
"""

        # Mapper
        mapper_dir = controller_dir / 'mapper'
        mapper_dir.mkdir(exist_ok=True)

        files[str(mapper_dir / 'LoanDtoMapper.java')] = f"""package {pkg}.adapter.input.rest.mapper;

import {pkg}.domain.model.*;
import {pkg}.adapter.input.rest.dto.*;

/**
 * Maps between REST DTOs and domain models.
 */
public class LoanDtoMapper {{
    
    public static LoanApplication toDomain(LoanRequestDto dto) {{
        LoanApplication loan = new LoanApplication();
        loan.setAmount(dto.getAmount());
        loan.setTermMonths(dto.getTermMonths());
        
        ApplicantInfo applicant = new ApplicantInfo();
        applicant.setFirstName(dto.getFirstName());
        applicant.setLastName(dto.getLastName());
        applicant.setSsn(dto.getSsn());
        applicant.setEmail(dto.getEmail());
        loan.setApplicant(applicant);
        
        return loan;
    }}
    
    public static LoanResponseDto toDto(LoanApplication domain) {{
        LoanResponseDto dto = new LoanResponseDto();
        dto.setLoanId(domain.getId());
        dto.setApplicantName(domain.getApplicant().getFullName());
        dto.setAmount(domain.getAmount());
        dto.setTermMonths(domain.getTermMonths());
        dto.setCreditScore(domain.getCreditScore() != null ? domain.getCreditScore().getScore() : null);
        dto.setStatus(domain.getStatus().name());
        dto.setAppliedAt(domain.getAppliedAt());
        dto.setProcessedAt(domain.getProcessedAt());
        return dto;
    }}
}}
"""

        return files

    def _generate_soap_adapter(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate SOAP adapter (endpoint + config)."""
        files = {}
        
        # Endpoint
        endpoint_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'adapter' / 'input' / 'soap'
        endpoint_dir.mkdir(parents=True, exist_ok=True)

        files[str(endpoint_dir / 'LoanSoapEndpoint.java')] = f"""package {pkg}.adapter.input.soap;

import {pkg}.domain.port.input.LoanApplicationUseCase;
import {pkg}.domain.model.LoanApplication;
import {pkg}.adapter.input.soap.dto.LoanApplicationRequest;
import {pkg}.adapter.input.soap.dto.LoanApplicationResponse;
import {pkg}.adapter.input.soap.mapper.LoanSoapMapper;

import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

/**
 * SOAP adapter for loan application use case.
 */
@Endpoint
public class LoanSoapEndpoint {{
    
    private static final String NAMESPACE_URI = "http://example.com/tibco_migration/loan";
    
    private final LoanApplicationUseCase loanUseCase;
    
    public LoanSoapEndpoint(LoanApplicationUseCase loanUseCase) {{
        this.loanUseCase = loanUseCase;
    }}
    
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "LoanApplicationRequest")
    @ResponsePayload
    public LoanApplicationResponse applyForLoan(@RequestPayload LoanApplicationRequest request) {{
        // Map SOAP request to domain
        LoanApplication domain = LoanSoapMapper.toDomain(request);
        
        // Execute use case (same as REST!)
        LoanApplication result = loanUseCase.applyForLoan(domain);
        
        // Map domain to SOAP response
        return LoanSoapMapper.toSoap(result);
    }}
}}
"""

        # SOAP DTOs (JAXB annotated)
        dto_dir = endpoint_dir / 'dto'
        dto_dir.mkdir(exist_ok=True)

        files[str(dto_dir / 'LoanApplicationRequest.java')] = f"""package {pkg}.adapter.input.soap.dto;

import jakarta.xml.bind.annotation.*;
import java.math.BigDecimal;

@XmlRootElement(name = "LoanApplicationRequest", namespace = "http://example.com/tibco_migration/loan")
@XmlAccessorType(XmlAccessType.FIELD)
public class LoanApplicationRequest {{
    
    @XmlElement(required = true)
    private String firstName;
    
    @XmlElement(required = true)
    private String lastName;
    
    @XmlElement(required = true)
    private String ssn;
    
    @XmlElement
    private String email;
    
    @XmlElement(required = true)
    private BigDecimal amount;
    
    @XmlElement(required = true)
    private Integer termMonths;

    // Getters and setters
    public String getFirstName() {{ return firstName; }}
    public void setFirstName(String firstName) {{ this.firstName = firstName; }}

    public String getLastName() {{ return lastName; }}
    public void setLastName(String lastName) {{ this.lastName = lastName; }}

    public String getSsn() {{ return ssn; }}
    public void setSsn(String ssn) {{ this.ssn = ssn; }}

    public String getEmail() {{ return email; }}
    public void setEmail(String email) {{ this.email = email; }}

    public BigDecimal getAmount() {{ return amount; }}
    public void setAmount(BigDecimal amount) {{ this.amount = amount; }}

    public Integer getTermMonths() {{ return termMonths; }}
    public void setTermMonths(Integer termMonths) {{ this.termMonths = termMonths; }}
}}
"""

        files[str(dto_dir / 'LoanApplicationResponse.java')] = f"""package {pkg}.adapter.input.soap.dto;

import jakarta.xml.bind.annotation.*;
import java.math.BigDecimal;

@XmlRootElement(name = "LoanApplicationResponse", namespace = "http://example.com/tibco_migration/loan")
@XmlAccessorType(XmlAccessType.FIELD)
public class LoanApplicationResponse {{
    
    @XmlElement
    private String loanId;
    
    @XmlElement
    private String applicantName;
    
    @XmlElement
    private BigDecimal amount;
    
    @XmlElement
    private Integer creditScore;
    
    @XmlElement
    private String status;

    // Getters and setters
    public String getLoanId() {{ return loanId; }}
    public void setLoanId(String loanId) {{ this.loanId = loanId; }}

    public String getApplicantName() {{ return applicantName; }}
    public void setApplicantName(String applicantName) {{ this.applicantName = applicantName; }}

    public BigDecimal getAmount() {{ return amount; }}
    public void setAmount(BigDecimal amount) {{ this.amount = amount; }}

    public Integer getCreditScore() {{ return creditScore; }}
    public void setCreditScore(Integer creditScore) {{ this.creditScore = creditScore; }}

    public String getStatus() {{ return status; }}
    public void setStatus(String status) {{ this.status = status; }}
}}
"""

        # SOAP Mapper
        mapper_dir = endpoint_dir / 'mapper'
        mapper_dir.mkdir(exist_ok=True)

        files[str(mapper_dir / 'LoanSoapMapper.java')] = f"""package {pkg}.adapter.input.soap.mapper;

import {pkg}.domain.model.*;
import {pkg}.adapter.input.soap.dto.*;

/**
 * Maps between SOAP DTOs and domain models.
 */
public class LoanSoapMapper {{
    
    public static LoanApplication toDomain(LoanApplicationRequest request) {{
        LoanApplication loan = new LoanApplication();
        loan.setAmount(request.getAmount());
        loan.setTermMonths(request.getTermMonths());
        
        ApplicantInfo applicant = new ApplicantInfo();
        applicant.setFirstName(request.getFirstName());
        applicant.setLastName(request.getLastName());
        applicant.setSsn(request.getSsn());
        applicant.setEmail(request.getEmail());
        loan.setApplicant(applicant);
        
        return loan;
    }}
    
    public static LoanApplicationResponse toSoap(LoanApplication domain) {{
        LoanApplicationResponse response = new LoanApplicationResponse();
        response.setLoanId(domain.getId());
        response.setApplicantName(domain.getApplicant().getFullName());
        response.setAmount(domain.getAmount());
        response.setCreditScore(domain.getCreditScore() != null ? domain.getCreditScore().getScore() : null);
        response.setStatus(domain.getStatus().name());
        return response;
    }}
}}
"""

        # SOAP Config
        config_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'adapter' / 'input' / 'soap' / 'config'
        config_dir.mkdir(parents=True, exist_ok=True)

        files[str(config_dir / 'WebServiceConfig.java')] = f"""package {pkg}.adapter.input.soap.config;

import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.ws.config.annotation.EnableWs;
import org.springframework.ws.config.annotation.WsConfigurerAdapter;
import org.springframework.ws.transport.http.MessageDispatcherServlet;
import org.springframework.ws.wsdl.wsdl11.DefaultWsdl11Definition;
import org.springframework.xml.xsd.SimpleXsdSchema;
import org.springframework.xml.xsd.XsdSchema;

@EnableWs
@Configuration
public class WebServiceConfig extends WsConfigurerAdapter {{

    @Bean
    public ServletRegistrationBean<MessageDispatcherServlet> messageDispatcherServlet(
            ApplicationContext applicationContext) {{
        MessageDispatcherServlet servlet = new MessageDispatcherServlet();
        servlet.setApplicationContext(applicationContext);
        servlet.setTransformWsdlLocations(true);
        return new ServletRegistrationBean<>(servlet, "/ws/*");
    }}

    @Bean(name = "loanApplication")
    public DefaultWsdl11Definition defaultWsdl11Definition(XsdSchema loanRequestSchema) {{
        DefaultWsdl11Definition wsdl11Definition = new DefaultWsdl11Definition();
        wsdl11Definition.setPortTypeName("LoanApplicationPort");
        wsdl11Definition.setLocationUri("/ws");
        wsdl11Definition.setTargetNamespace("http://example.com/tibco_migration/loan");
        wsdl11Definition.setSchema(loanRequestSchema);
        return wsdl11Definition;
    }}

    @Bean
    public XsdSchema loanRequestSchema() {{
        return new SimpleXsdSchema(new ClassPathResource("xsd/loan_request.xsd"));
    }}
}}
"""

        # XSD schema
        xsd_dir = out / 'src' / 'main' / 'resources' / 'xsd'
        xsd_dir.mkdir(parents=True, exist_ok=True)

        files[str(xsd_dir / 'loan_request.xsd')] = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:tns="http://example.com/tibco_migration/loan"
           targetNamespace="http://example.com/tibco_migration/loan"
           elementFormDefault="qualified">

    <xs:element name="LoanApplicationRequest">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="firstName" type="xs:string"/>
                <xs:element name="lastName" type="xs:string"/>
                <xs:element name="ssn" type="xs:string"/>
                <xs:element name="email" type="xs:string" minOccurs="0"/>
                <xs:element name="amount" type="xs:decimal"/>
                <xs:element name="termMonths" type="xs:int"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>

    <xs:element name="LoanApplicationResponse">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="loanId" type="xs:string"/>
                <xs:element name="applicantName" type="xs:string"/>
                <xs:element name="amount" type="xs:decimal"/>
                <xs:element name="creditScore" type="xs:int" minOccurs="0"/>
                <xs:element name="status" type="xs:string"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>

</xs:schema>
"""

        return files

    # ==================== OUTPUT ADAPTERS ====================

    def _generate_persistence_adapter(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate JPA persistence adapter."""
        files = {}
        
        adapter_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'adapter' / 'output' / 'persistence'
        adapter_dir.mkdir(parents=True, exist_ok=True)

        # JPA Repository Adapter
        files[str(adapter_dir / 'LoanRepositoryAdapter.java')] = f"""package {pkg}.adapter.output.persistence;

import {pkg}.domain.model.LoanApplication;
import {pkg}.domain.port.output.LoanRepository;
import {pkg}.adapter.output.persistence.entity.LoanEntity;

import org.springframework.stereotype.Component;
import java.util.Optional;

/**
 * JPA adapter implementing domain repository port.
 */
@Component
public class LoanRepositoryAdapter implements LoanRepository {{
    
    private final LoanJpaRepository jpaRepository;
    
    public LoanRepositoryAdapter(LoanJpaRepository jpaRepository) {{
        this.jpaRepository = jpaRepository;
    }}
    
    @Override
    public LoanApplication save(LoanApplication loan) {{
        LoanEntity entity = LoanEntityMapper.toEntity(loan);
        LoanEntity saved = jpaRepository.save(entity);
        return LoanEntityMapper.toDomain(saved);
    }}
    
    @Override
    public Optional<LoanApplication> findById(String id) {{
        return jpaRepository.findById(id)
                .map(LoanEntityMapper::toDomain);
    }}
}}
"""

        # Spring Data JPA Repository
        files[str(adapter_dir / 'LoanJpaRepository.java')] = f"""package {pkg}.adapter.output.persistence;

import {pkg}.adapter.output.persistence.entity.LoanEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LoanJpaRepository extends JpaRepository<LoanEntity, String> {{
}}
"""

        # JPA Entity
        entity_dir = adapter_dir / 'entity'
        entity_dir.mkdir(exist_ok=True)

        files[str(entity_dir / 'LoanEntity.java')] = f"""package {pkg}.adapter.output.persistence.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * JPA entity for loan persistence.
 * Separate from domain model to keep domain clean.
 */
@Entity
@Table(name = "loans")
public class LoanEntity {{
    
    @Id
    private String id;
    
    private String firstName;
    private String lastName;
    private String ssn;
    private String email;
    
    private BigDecimal amount;
    private Integer termMonths;
    private Integer creditScore;
    
    @Enumerated(EnumType.STRING)
    private LoanStatusEntity status;
    
    private LocalDateTime appliedAt;
    private LocalDateTime processedAt;

    // Getters and setters
    public String getId() {{ return id; }}
    public void setId(String id) {{ this.id = id; }}

    public String getFirstName() {{ return firstName; }}
    public void setFirstName(String firstName) {{ this.firstName = firstName; }}

    public String getLastName() {{ return lastName; }}
    public void setLastName(String lastName) {{ this.lastName = lastName; }}

    public String getSsn() {{ return ssn; }}
    public void setSsn(String ssn) {{ this.ssn = ssn; }}

    public String getEmail() {{ return email; }}
    public void setEmail(String email) {{ this.email = email; }}

    public BigDecimal getAmount() {{ return amount; }}
    public void setAmount(BigDecimal amount) {{ this.amount = amount; }}

    public Integer getTermMonths() {{ return termMonths; }}
    public void setTermMonths(Integer termMonths) {{ this.termMonths = termMonths; }}

    public Integer getCreditScore() {{ return creditScore; }}
    public void setCreditScore(Integer creditScore) {{ this.creditScore = creditScore; }}

    public LoanStatusEntity getStatus() {{ return status; }}
    public void setStatus(LoanStatusEntity status) {{ this.status = status; }}

    public LocalDateTime getAppliedAt() {{ return appliedAt; }}
    public void setAppliedAt(LocalDateTime appliedAt) {{ this.appliedAt = appliedAt; }}

    public LocalDateTime getProcessedAt() {{ return processedAt; }}
    public void setProcessedAt(LocalDateTime processedAt) {{ this.processedAt = processedAt; }}
}}

enum LoanStatusEntity {{
    PENDING,
    APPROVED,
    REJECTED
}}
"""

        # Entity Mapper
        files[str(adapter_dir / 'LoanEntityMapper.java')] = f"""package {pkg}.adapter.output.persistence;

import {pkg}.domain.model.*;
import {pkg}.adapter.output.persistence.entity.*;

/**
 * Maps between JPA entities and domain models.
 */
public class LoanEntityMapper {{
    
    public static LoanEntity toEntity(LoanApplication domain) {{
        LoanEntity entity = new LoanEntity();
        entity.setId(domain.getId());
        entity.setFirstName(domain.getApplicant().getFirstName());
        entity.setLastName(domain.getApplicant().getLastName());
        entity.setSsn(domain.getApplicant().getSsn());
        entity.setEmail(domain.getApplicant().getEmail());
        entity.setAmount(domain.getAmount());
        entity.setTermMonths(domain.getTermMonths());
        entity.setCreditScore(domain.getCreditScore() != null ? domain.getCreditScore().getScore() : null);
        entity.setStatus(LoanStatusEntity.valueOf(domain.getStatus().name()));
        entity.setAppliedAt(domain.getAppliedAt());
        entity.setProcessedAt(domain.getProcessedAt());
        return entity;
    }}
    
    public static LoanApplication toDomain(LoanEntity entity) {{
        LoanApplication domain = new LoanApplication();
        domain.setId(entity.getId());
        
        ApplicantInfo applicant = new ApplicantInfo();
        applicant.setFirstName(entity.getFirstName());
        applicant.setLastName(entity.getLastName());
        applicant.setSsn(entity.getSsn());
        applicant.setEmail(entity.getEmail());
        domain.setApplicant(applicant);
        
        domain.setAmount(entity.getAmount());
        domain.setTermMonths(entity.getTermMonths());
        if (entity.getCreditScore() != null) {{
            domain.setCreditScore(new CreditScore(entity.getCreditScore()));
        }}
        domain.setStatus(LoanStatus.valueOf(entity.getStatus().name()));
        domain.setAppliedAt(entity.getAppliedAt());
        domain.setProcessedAt(entity.getProcessedAt());
        
        return domain;
    }}
}}
"""

        return files

    def _generate_http_gateway_adapter(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate HTTP client adapter for external service."""
        files = {}
        
        adapter_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'adapter' / 'output' / 'http'
        adapter_dir.mkdir(parents=True, exist_ok=True)

        files[str(adapter_dir / 'CreditScoreHttpAdapter.java')] = f"""package {pkg}.adapter.output.http;

import {pkg}.domain.model.ApplicantInfo;
import {pkg}.domain.model.CreditScore;
import {pkg}.domain.port.output.CreditScoreGateway;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

/**
 * HTTP adapter for credit score checking.
 * Calls external credit score service.
 */
@Component
public class CreditScoreHttpAdapter implements CreditScoreGateway {{
    
    private final WebClient webClient;
    
    public CreditScoreHttpAdapter(
            @Value("${{creditscore.service.url:http://localhost:8082/creditscore}}") String baseUrl) {{
        this.webClient = WebClient.builder()
                .baseUrl(baseUrl)
                .build();
    }}
    
    @Override
    public CreditScore checkCredit(ApplicantInfo applicant) {{
        // Call external service (simplified)
        try {{
            Integer score = webClient.post()
                    .uri("/check")
                    .bodyValue(applicant)
                    .retrieve()
                    .bodyToMono(Integer.class)
                    .block();
            
            return new CreditScore(score != null ? score : 650);
        }} catch (Exception e) {{
            // Fallback score if service unavailable
            return new CreditScore(650);
        }}
    }}
}}
"""

        return files

    def _generate_jms_adapter(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate JMS messaging adapter."""
        files = {}
        
        adapter_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'adapter' / 'output' / 'messaging'
        adapter_dir.mkdir(parents=True, exist_ok=True)

        files[str(adapter_dir / 'NotificationJmsAdapter.java')] = f"""package {pkg}.adapter.output.messaging;

import {pkg}.domain.model.LoanApplication;
import {pkg}.domain.port.output.NotificationGateway;

import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Component;

/**
 * JMS adapter for sending notifications.
 */
@Component
public class NotificationJmsAdapter implements NotificationGateway {{
    
    private final JmsTemplate jmsTemplate;
    
    public NotificationJmsAdapter(JmsTemplate jmsTemplate) {{
        this.jmsTemplate = jmsTemplate;
    }}
    
    @Override
    public void sendApplicationNotification(LoanApplication loan) {{
        String message = String.format(
            "Loan Application %s for %s - Status: %s",
            loan.getId(),
            loan.getApplicant().getFullName(),
            loan.getStatus()
        );
        
        jmsTemplate.convertAndSend("loan.notifications", message);
    }}
}}
"""

        return files

    # ==================== CONFIGURATION ====================

    def _generate_application_class(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate Spring Boot application class."""
        files = {}
        
        app_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/')
        app_dir.mkdir(parents=True, exist_ok=True)

        files[str(app_dir / 'HexagonalApplication.java')] = f"""package {pkg};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Spring Boot application using Hexagonal Architecture.
 */
@SpringBootApplication
public class HexagonalApplication {{

    public static void main(String[] args) {{
        SpringApplication.run(HexagonalApplication.class, args);
    }}
}}
"""

        return files

    def _generate_adapter_config(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate adapter configuration."""
        files = {}
        
        config_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'config'
        config_dir.mkdir(parents=True, exist_ok=True)

        files[str(config_dir / 'AdapterConfig.java')] = f"""package {pkg}.config;

import {pkg}.domain.service.LoanApplicationService;
import {pkg}.domain.port.input.LoanApplicationUseCase;
import {pkg}.domain.port.output.LoanRepository;
import {pkg}.domain.port.output.CreditScoreGateway;
import {pkg}.domain.port.output.NotificationGateway;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * Configuration for hexagonal architecture.
 * This is where we wire the domain service with adapter implementations.
 * 
 * The domain service is pure Java - this config adds Spring framework support.
 */
@Configuration
@EnableJpaRepositories(basePackages = "{{pkg}}.adapter.output.persistence")
@EnableTransactionManagement
public class AdapterConfig {{
    
    /**
     * Create the domain service bean.
     * Wire it with output port implementations (adapters).
     * 
     * @param loanRepository JPA persistence adapter
     * @param creditScoreGateway HTTP gateway adapter
     * @param notificationGateway JMS messaging adapter
     * @return The use case implementation
     */
    @Bean
    public LoanApplicationUseCase loanApplicationUseCase(
            LoanRepository loanRepository,
            CreditScoreGateway creditScoreGateway,
            NotificationGateway notificationGateway) {{
        return new LoanApplicationService(
            loanRepository,
            creditScoreGateway,
            notificationGateway
        );
    }}
}}
""".replace('{{pkg}}', pkg)

        return files

    def _generate_application_yml(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate application.yml configuration."""
        files = {}
        
        resources_dir = out / 'src' / 'main' / 'resources'
        resources_dir.mkdir(parents=True, exist_ok=True)

        port = 8080 if self.service_type == 'rest' else 8081 if self.service_type == 'soap' else 8080

        files[str(resources_dir / 'application.yml')] = f"""server:
  port: {port}

spring:
  application:
    name: tibco-migration-hexagonal-{self.service_type}
  
  datasource:
    url: jdbc:h2:mem:loandb
    driver-class-name: org.h2.Driver
    username: sa
    password: 
  
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
    properties:
      hibernate:
        format_sql: true
  
  h2:
    console:
      enabled: true
      path: /h2-console
  
  artemis:
    mode: embedded

# External service URLs
creditscore:
  service:
    url: http://localhost:8082/creditscore

logging:
  level:
    {pkg.replace('.', '/')}: DEBUG
    org.springframework.web: INFO
    org.springframework.ws: DEBUG
"""

        return files

    def _generate_pom(self, out: Path) -> Dict[str, str]:
        """Generate pom.xml with all dependencies."""
        files = {}

        deps = []
        if self.service_type in ['rest', 'combined']:
            deps.append("""        <!-- Spring Boot Starter Web (REST) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        
        <!-- Spring Boot Starter Validation -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>""")

        if self.service_type in ['soap', 'combined']:
            deps.append("""        <!-- Spring Boot Starter Web Services (SOAP) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web-services</artifactId>
        </dependency>
        
        <!-- WSDL4J for WSDL generation -->
        <dependency>
            <groupId>wsdl4j</groupId>
            <artifactId>wsdl4j</artifactId>
        </dependency>""")

        dependencies = '\n\n'.join(deps)

        files[str(out / 'pom.xml')] = f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>tibco-migration-hexagonal-{self.service_type}</artifactId>
    <version>0.1.0</version>
    <packaging>jar</packaging>
    <name>TIBCO Migration Hexagonal Architecture ({self.service_type.upper()})</name>

    <properties>
        <java.version>17</java.version>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
{dependencies}

        <!-- Spring Boot Starter Data JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- Spring Boot Starter Artemis (JMS) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-artemis</artifactId>
        </dependency>

        <!-- Spring Boot WebFlux for WebClient -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-webflux</artifactId>
        </dependency>

        <!-- H2 Database for testing -->
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Spring Boot Starter Test -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
"""

        return files

    def _generate_readme(self, out: Path) -> Dict[str, str]:
        """Generate README for hexagonal architecture project."""
        files = {}

        service_urls = ""
        if self.service_type in ['rest', 'combined']:
            service_urls += """
### REST API
- Base URL: `http://localhost:8080/api/loans`
- Apply for loan: `POST /api/loans/apply`
- Get loan: `GET /api/loans/{{loanId}}`
"""

        if self.service_type in ['soap', 'combined']:
            service_urls += """
### SOAP Web Service
- WSDL: `http://localhost:8081/ws/loanApplication.wsdl`
- Endpoint: `http://localhost:8081/ws`
"""

        files[str(out / 'README.md')] = f"""# TIBCO Migration - Hexagonal Architecture ({self.service_type.upper()})

This project was generated using **Hexagonal Architecture** (Ports & Adapters pattern).

## Architecture Overview

```
Domain (Core Business Logic)
    ↑
Input Ports (Use Cases)
    ↑
Adapters ({self.service_type.upper()})
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
{service_urls}

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
"""

        return files
