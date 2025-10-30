package com.example.tibco_migration.dto;

import java.math.BigDecimal;


public class LoanApplicationRequest {
    private String customerID;
    private BigDecimal loanAmount;
    private String loanType;
    private Integer loanTermMonths;
    private String applicantName;
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
