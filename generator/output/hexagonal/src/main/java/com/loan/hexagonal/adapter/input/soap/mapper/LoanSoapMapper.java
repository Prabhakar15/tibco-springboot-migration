package com.loan.hexagonal.adapter.input.soap.mapper;

import com.loan.hexagonal.domain.model.*;
import com.loan.hexagonal.adapter.input.soap.dto.*;

/**
 * Maps between SOAP DTOs and domain models.
 */
public class LoanSoapMapper {
    
    public static LoanApplication toDomain(LoanApplicationRequest request) {
        LoanApplication loan = new LoanApplication();
        loan.setAmount(request.getAmount());
        loan.setTermMonths(request.getTermMonths());
        
        ApplicantInfo applicant = new ApplicantInfo();
        applicant.setFirstName(request.getFirstName());
        applicant.setLastName(request.getLastName());
        applicant.setSsn(request.getSsn());
        applicant.setEmail(request.getEmail());
        loan.setApplicant(applicant);
        
        return loan;
    }
    
    public static LoanApplicationResponse toSoap(LoanApplication domain) {
        LoanApplicationResponse response = new LoanApplicationResponse();
        response.setLoanId(domain.getId());
        response.setApplicantName(domain.getApplicant().getFullName());
        response.setAmount(domain.getAmount());
        response.setCreditScore(domain.getCreditScore() != null ? domain.getCreditScore().getScore() : null);
        response.setStatus(domain.getStatus().name());
        return response;
    }
}
