package com.loan.hexagonal.domain.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Domain model for Loan Application.
 * Pure business entity with no framework dependencies.
 */
public class LoanApplication {
    
    private String id;
    private ApplicantInfo applicant;
    private BigDecimal amount;
    private Integer termMonths;
    private CreditScore creditScore;
    private LoanStatus status;
    private LocalDateTime appliedAt;
    private LocalDateTime processedAt;

    // Constructor
    public LoanApplication() {
        this.appliedAt = LocalDateTime.now();
        this.status = LoanStatus.PENDING;
    }

    // Business methods
    public void approve() {
        if (this.creditScore == null || this.creditScore.getScore() < 600) {
            throw new IllegalStateException("Cannot approve loan with credit score < 600");
        }
        this.status = LoanStatus.APPROVED;
        this.processedAt = LocalDateTime.now();
    }

    public void reject(String reason) {
        this.status = LoanStatus.REJECTED;
        this.processedAt = LocalDateTime.now();
    }

    public boolean isApproved() {
        return LoanStatus.APPROVED.equals(this.status);
    }

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public ApplicantInfo getApplicant() { return applicant; }
    public void setApplicant(ApplicantInfo applicant) { this.applicant = applicant; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public Integer getTermMonths() { return termMonths; }
    public void setTermMonths(Integer termMonths) { this.termMonths = termMonths; }

    public CreditScore getCreditScore() { return creditScore; }
    public void setCreditScore(CreditScore creditScore) { this.creditScore = creditScore; }

    public LoanStatus getStatus() { return status; }
    public void setStatus(LoanStatus status) { this.status = status; }

    public LocalDateTime getAppliedAt() { return appliedAt; }
    public void setAppliedAt(LocalDateTime appliedAt) { this.appliedAt = appliedAt; }

    public LocalDateTime getProcessedAt() { return processedAt; }
    public void setProcessedAt(LocalDateTime processedAt) { this.processedAt = processedAt; }
}
