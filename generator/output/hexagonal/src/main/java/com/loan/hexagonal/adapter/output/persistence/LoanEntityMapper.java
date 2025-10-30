package com.loan.hexagonal.adapter.output.persistence;

import com.loan.hexagonal.domain.model.*;
import com.loan.hexagonal.adapter.output.persistence.entity.*;

/**
 * Maps between JPA entities and domain models.
 */
public class LoanEntityMapper {
    
    public static LoanEntity toEntity(LoanApplication domain) {
        LoanEntity entity = new LoanEntity();
        entity.setId(domain.getId());
        entity.setFirstName(domain.getApplicant().getFirstName());
        entity.setLastName(domain.getApplicant().getLastName());
        entity.setSsn(domain.getApplicant().getSsn());
        entity.setEmail(domain.getApplicant().getEmail());
        entity.setAmount(domain.getAmount());
        entity.setTermMonths(domain.getTermMonths());
        entity.setCreditScore(domain.getCreditScore() != null ? domain.getCreditScore().getScore() : null);
        entity.setStatus(LoanStatusEntity.valueOf(domain.getStatus().name()));
        entity.setAppliedAt(domain.getAppliedAt());
        entity.setProcessedAt(domain.getProcessedAt());
        return entity;
    }
    
    public static LoanApplication toDomain(LoanEntity entity) {
        LoanApplication domain = new LoanApplication();
        domain.setId(entity.getId());
        
        ApplicantInfo applicant = new ApplicantInfo();
        applicant.setFirstName(entity.getFirstName());
        applicant.setLastName(entity.getLastName());
        applicant.setSsn(entity.getSsn());
        applicant.setEmail(entity.getEmail());
        domain.setApplicant(applicant);
        
        domain.setAmount(entity.getAmount());
        domain.setTermMonths(entity.getTermMonths());
        if (entity.getCreditScore() != null) {
            domain.setCreditScore(new CreditScore(entity.getCreditScore()));
        }
        domain.setStatus(LoanStatus.valueOf(entity.getStatus().name()));
        domain.setAppliedAt(entity.getAppliedAt());
        domain.setProcessedAt(entity.getProcessedAt());
        
        return domain;
    }
}
