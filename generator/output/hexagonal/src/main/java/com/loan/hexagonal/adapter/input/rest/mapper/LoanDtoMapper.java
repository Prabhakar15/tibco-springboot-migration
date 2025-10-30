package com.loan.hexagonal.adapter.input.rest.mapper;

import com.loan.hexagonal.domain.model.*;
import com.loan.hexagonal.adapter.input.rest.dto.*;

/**
 * Maps between REST DTOs and domain models.
 */
public class LoanDtoMapper {
    
    public static LoanApplication toDomain(LoanRequestDto dto) {
        LoanApplication loan = new LoanApplication();
        loan.setAmount(dto.getAmount());
        loan.setTermMonths(dto.getTermMonths());
        
        ApplicantInfo applicant = new ApplicantInfo();
        applicant.setFirstName(dto.getFirstName());
        applicant.setLastName(dto.getLastName());
        applicant.setSsn(dto.getSsn());
        applicant.setEmail(dto.getEmail());
        loan.setApplicant(applicant);
        
        return loan;
    }
    
    public static LoanResponseDto toDto(LoanApplication domain) {
        LoanResponseDto dto = new LoanResponseDto();
        dto.setLoanId(domain.getId());
        dto.setApplicantName(domain.getApplicant().getFullName());
        dto.setAmount(domain.getAmount());
        dto.setTermMonths(domain.getTermMonths());
        dto.setCreditScore(domain.getCreditScore() != null ? domain.getCreditScore().getScore() : null);
        dto.setStatus(domain.getStatus().name());
        dto.setAppliedAt(domain.getAppliedAt());
        dto.setProcessedAt(domain.getProcessedAt());
        return dto;
    }
}
