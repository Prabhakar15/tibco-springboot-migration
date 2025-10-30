package com.loan.hexagonal.adapter.input.soap.dto;

import jakarta.xml.bind.annotation.*;
import java.math.BigDecimal;

@XmlRootElement(name = "LoanApplicationRequest", namespace = "http://example.com/tibco_migration/loan")
@XmlAccessorType(XmlAccessType.FIELD)
public class LoanApplicationRequest {
    
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
}
