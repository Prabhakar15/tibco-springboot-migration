"""Small Java templates used by generator to create DTOs and controller/service skeletons."""

CREDIT_SCORE_REQUEST_TEMPLATE = '''package {package}.dto;

public class CreditScoreRequest {{
    private String customerId;
    private String applicantName;

    public CreditScoreRequest(String customerId, String applicantName) {{
        this.customerId = customerId;
        this.applicantName = applicantName;
    }}

    public String getCustomerId() {{
        return customerId;
    }}

    public void setCustomerId(String customerId) {{
        this.customerId = customerId;
    }}

    public String getApplicantName() {{
        return applicantName;
    }}

    public void setApplicantName(String applicantName) {{
        this.applicantName = applicantName;
    }}
}}
'''

REPOSITORY_TEMPLATE = '''package {package}.repository;

import {package}.entity.LoanEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface {repo} extends JpaRepository<LoanEntity, String> {{
}}
'''

CREDIT_SCORE_RESPONSE_TEMPLATE = '''package {package}.dto;

public class CreditScoreResponse {{
    private Integer score;
    private String creditHistory;
    private String riskLevel;

    public Integer getScore() {{
        return score;
    }}

    public void setScore(Integer score) {{
        this.score = score;
    }}

    public String getCreditHistory() {{
        return creditHistory;
    }}

    public void setCreditHistory(String creditHistory) {{
        this.creditHistory = creditHistory;
    }}

    public String getRiskLevel() {{
        return riskLevel;
    }}

    public void setRiskLevel(String riskLevel) {{
        this.riskLevel = riskLevel;
    }}
}}
'''

ENTITY_TEMPLATE = '''package {package}.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;
import java.math.BigDecimal;

@Entity
@Table(name = "LOANS")
public class LoanEntity {{
    @Id
    private String loanId;
    private String customerId;
    private String applicantName;
    private BigDecimal loanAmount;
    private String loanType;
    private Integer loanTermMonths;
    private String contactEmail;
    private LocalDateTime applicationDate;
    private String status;
    private BigDecimal approvedAmount;
    private String rejectionReason;

    public String getLoanId() {{
        return loanId;
    }}

    public void setLoanId(String loanId) {{
        this.loanId = loanId;
    }}

    public String getCustomerId() {{
        return customerId;
    }}

    public void setCustomerId(String customerId) {{
        this.customerId = customerId;
    }}

    public String getApplicantName() {{
        return applicantName;
    }}

    public void setApplicantName(String applicantName) {{
        this.applicantName = applicantName;
    }}

    public BigDecimal getLoanAmount() {{
        return loanAmount;
    }}

    public void setLoanAmount(BigDecimal loanAmount) {{
        this.loanAmount = loanAmount;
    }}

    public String getLoanType() {{
        return loanType;
    }}

    public void setLoanType(String loanType) {{
        this.loanType = loanType;
    }}

    public Integer getLoanTermMonths() {{
        return loanTermMonths;
    }}

    public void setLoanTermMonths(Integer loanTermMonths) {{
        this.loanTermMonths = loanTermMonths;
    }}

    public String getContactEmail() {{
        return contactEmail;
    }}

    public void setContactEmail(String contactEmail) {{
        this.contactEmail = contactEmail;
    }}

    public LocalDateTime getApplicationDate() {{
        return applicationDate;
    }}

    public void setApplicationDate(LocalDateTime applicationDate) {{
        this.applicationDate = applicationDate;
    }}

    public String getStatus() {{
        return status;
    }}

    public void setStatus(String status) {{
        this.status = status;
    }}

    public BigDecimal getApprovedAmount() {{
        return approvedAmount;
    }}

    public void setApprovedAmount(BigDecimal approvedAmount) {{
        this.approvedAmount = approvedAmount;
    }}

    public String getRejectionReason() {{
        return rejectionReason;
    }}

    public void setRejectionReason(String rejectionReason) {{
        this.rejectionReason = rejectionReason;
    }}
}}
'''

DTO_CLASS = '''package {package}.dto;

{imports}
public class {class_name} {{
{fields}

{getters_setters}
}}
'''

CONTROLLER_TEMPLATE = '''package {package}.controller;

import {package}.dto.{request};
import {package}.dto.{response};
import {package}.service.{service};

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/{root}")
public class {controller} {{

    private final {service} service;

    public {controller}({service} service) {{
        this.service = service;
    }}

    @PostMapping("/apply")
    public ResponseEntity<{response}> apply(@Valid @RequestBody {request} request) {{
        {response_var} resp = service.applyForLoan(request);
        return ResponseEntity.ok(resp);
    }}
}}
'''

SERVICE_TEMPLATE = '''package {package}.service;

import {package}.dto.*;
import {package}.entity.LoanEntity;
import {package}.repository.{repo};

import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.LocalDateTime;
import java.util.UUID;

@Service
public class {service} {{

    private final WebClient webClient;
    private final {repo} repo;
    private final JmsTemplate jmsTemplate;

    public {service}(WebClient webClient, {repo} repo, JmsTemplate jmsTemplate) {{
        this.webClient = webClient;
        this.repo = repo;
        this.jmsTemplate = jmsTemplate;
    }}

    public {response} applyForLoan({request} req) {{
        // Create entity and map request data
        LoanEntity loan = new LoanEntity();
        loan.setLoanId(UUID.randomUUID().toString());
        loan.setCustomerId(req.getCustomerID());
        loan.setApplicantName(req.getApplicantName());
        loan.setLoanAmount(req.getLoanAmount());
        loan.setLoanType(req.getLoanType());
        loan.setLoanTermMonths(req.getLoanTermMonths());
        loan.setContactEmail(req.getContactEmail());
        loan.setApplicationDate(LocalDateTime.now());
        loan.setStatus("PENDING");
        
        // Save to database
        loan = repo.save(loan);

        // Call credit score service
        CreditScoreResponse creditScore = webClient.post()
            .uri("/check")
            .bodyValue(new CreditScoreRequest(loan.getCustomerId(), loan.getApplicantName()))
            .retrieve()
            .bodyToMono(CreditScoreResponse.class)
            .block();

        // Process score and update loan status
        String status;
        String message;
        if (creditScore.getScore() > 650) {{
            status = "APPROVED";
            message = "Loan application approved";
            loan.setApprovedAmount(loan.getLoanAmount());
        }} else {{
            status = "REJECTED";
            message = "Credit score below threshold";
            loan.setRejectionReason(message);
        }}
        
        loan.setStatus(status);
        repo.save(loan);

        // Send status via JMS
        jmsTemplate.convertAndSend("LoanStatusQueue", loan.getLoanId() + ":" + status);

        // Prepare response
        {response} response = new {response}();
        response.setLoanID(loan.getLoanId());
        response.setStatus(status);
        response.setMessage(message);
        if ("APPROVED".equals(status)) {{
            response.setApprovedAmount(loan.getApprovedAmount());
        }} else {{
            response.setRejectionReason(loan.getRejectionReason());
        }}
        
        return response;
    }}
}}
'''
