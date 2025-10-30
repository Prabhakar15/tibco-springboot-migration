package com.loan.hexagonal.adapter.input.soap.dto;

import jakarta.xml.bind.annotation.*;
import java.math.BigDecimal;

@XmlRootElement(name = "LoanApplicationResponse", namespace = "http://example.com/tibco_migration/loan")
@XmlAccessorType(XmlAccessType.FIELD)
public class LoanApplicationResponse {
    
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
    public String getLoanId() { return loanId; }
    public void setLoanId(String loanId) { this.loanId = loanId; }

    public String getApplicantName() { return applicantName; }
    public void setApplicantName(String applicantName) { this.applicantName = applicantName; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public Integer getCreditScore() { return creditScore; }
    public void setCreditScore(Integer creditScore) { this.creditScore = creditScore; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
