package com.example.tibco_migration.dto;


public class CreditScoreResponse {
    private String customerID;
    private Integer score;
    private String riskLevel;
    private String status;
    private String errorMessage;

    public String getCustomerID() { return customerID; }

    public Integer getScore() { return score; }

    public String getRiskLevel() { return riskLevel; }

    public String getStatus() { return status; }

    public String getErrorMessage() { return errorMessage; }

    public void setCustomerID(String customerID) { this.customerID = customerID; }

    public void setScore(Integer score) { this.score = score; }

    public void setRiskLevel(String riskLevel) { this.riskLevel = riskLevel; }

    public void setStatus(String status) { this.status = status; }

    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }
}
