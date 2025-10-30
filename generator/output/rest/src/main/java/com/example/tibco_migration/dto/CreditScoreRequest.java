package com.example.tibco_migration.dto;


public class CreditScoreRequest {
    private String customerID;
    private String applicantName;

    public String getCustomerID() { return customerID; }

    public String getApplicantName() { return applicantName; }

    public void setCustomerID(String customerID) { this.customerID = customerID; }

    public void setApplicantName(String applicantName) { this.applicantName = applicantName; }
}
