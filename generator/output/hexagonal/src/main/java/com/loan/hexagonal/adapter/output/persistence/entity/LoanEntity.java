package com.loan.hexagonal.adapter.output.persistence.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * JPA entity for loan persistence.
 * Separate from domain model to keep domain clean.
 */
@Entity
@Table(name = "loans")
public class LoanEntity {
    
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
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }

    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }

    public String getSsn() { return ssn; }
    public void setSsn(String ssn) { this.ssn = ssn; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public Integer getTermMonths() { return termMonths; }
    public void setTermMonths(Integer termMonths) { this.termMonths = termMonths; }

    public Integer getCreditScore() { return creditScore; }
    public void setCreditScore(Integer creditScore) { this.creditScore = creditScore; }

    public LoanStatusEntity getStatus() { return status; }
    public void setStatus(LoanStatusEntity status) { this.status = status; }

    public LocalDateTime getAppliedAt() { return appliedAt; }
    public void setAppliedAt(LocalDateTime appliedAt) { this.appliedAt = appliedAt; }

    public LocalDateTime getProcessedAt() { return processedAt; }
    public void setProcessedAt(LocalDateTime processedAt) { this.processedAt = processedAt; }
}

enum LoanStatusEntity {
    PENDING,
    APPROVED,
    REJECTED
}
