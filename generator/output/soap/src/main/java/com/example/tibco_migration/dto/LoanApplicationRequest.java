package com.example.tibco_migration.dto;

import jakarta.xml.bind.annotation.*;
import java.math.BigDecimal;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "customerID",
    "loanAmount",
    "loanType",
    "loanTermMonths",
    "applicantName",
    "contactEmail"
})
@XmlRootElement(name = "LoanApplicationRequest", namespace = "http://example.com/tibco_migration/loan")
public class LoanApplicationRequest {
    
    @XmlElement(namespace = "http://example.com/tibco_migration/loan", required = true)
    private String customerID;
    
    @XmlElement(namespace = "http://example.com/tibco_migration/loan", required = true)
    private BigDecimal loanAmount;
    
    @XmlElement(namespace = "http://example.com/tibco_migration/loan", required = true)
    private String loanType;
    
    @XmlElement(namespace = "http://example.com/tibco_migration/loan", required = true)
    private Integer loanTermMonths;
    
    @XmlElement(namespace = "http://example.com/tibco_migration/loan", required = true)
    private String applicantName;
    
    @XmlElement(namespace = "http://example.com/tibco_migration/loan")
    private String contactEmail;

    public String getCustomerID() { return customerID; }

    public BigDecimal getLoanAmount() { return loanAmount; }

    public String getLoanType() { return loanType; }

    public Integer getLoanTermMonths() { return loanTermMonths; }

    public String getApplicantName() { return applicantName; }

    public String getContactEmail() { return contactEmail; }

    public void setCustomerID(String customerID) { this.customerID = customerID; }

    public void setLoanAmount(BigDecimal loanAmount) { this.loanAmount = loanAmount; }

    public void setLoanType(String loanType) { this.loanType = loanType; }

    public void setLoanTermMonths(Integer loanTermMonths) { this.loanTermMonths = loanTermMonths; }

    public void setApplicantName(String applicantName) { this.applicantName = applicantName; }

    public void setContactEmail(String contactEmail) { this.contactEmail = contactEmail; }
}
