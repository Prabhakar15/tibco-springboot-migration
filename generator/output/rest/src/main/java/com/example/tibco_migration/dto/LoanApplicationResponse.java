package com.example.tibco_migration.dto;

import java.math.BigDecimal;


public class LoanApplicationResponse {
    private String loanID;
    private String status;
    private String message;
    private String rejectionReason;
    private BigDecimal approvedAmount;

    public String getLoanID() { return loanID; }

    public String getStatus() { return status; }

    public String getMessage() { return message; }

    public String getRejectionReason() { return rejectionReason; }

    public BigDecimal getApprovedAmount() { return approvedAmount; }

    public void setLoanID(String loanID) { this.loanID = loanID; }

    public void setStatus(String status) { this.status = status; }

    public void setMessage(String message) { this.message = message; }

    public void setRejectionReason(String rejectionReason) { this.rejectionReason = rejectionReason; }

    public void setApprovedAmount(BigDecimal approvedAmount) { this.approvedAmount = approvedAmount; }
}
