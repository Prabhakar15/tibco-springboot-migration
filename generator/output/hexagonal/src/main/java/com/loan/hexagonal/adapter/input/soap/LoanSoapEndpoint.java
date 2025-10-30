package com.loan.hexagonal.adapter.input.soap;

import com.loan.hexagonal.domain.port.input.LoanApplicationUseCase;
import com.loan.hexagonal.domain.model.LoanApplication;
import com.loan.hexagonal.adapter.input.soap.dto.LoanApplicationRequest;
import com.loan.hexagonal.adapter.input.soap.dto.LoanApplicationResponse;
import com.loan.hexagonal.adapter.input.soap.mapper.LoanSoapMapper;

import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

/**
 * SOAP adapter for loan application use case.
 */
@Endpoint
public class LoanSoapEndpoint {
    
    private static final String NAMESPACE_URI = "http://example.com/tibco_migration/loan";
    
    private final LoanApplicationUseCase loanUseCase;
    
    public LoanSoapEndpoint(LoanApplicationUseCase loanUseCase) {
        this.loanUseCase = loanUseCase;
    }
    
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "LoanApplicationRequest")
    @ResponsePayload
    public LoanApplicationResponse applyForLoan(@RequestPayload LoanApplicationRequest request) {
        // Map SOAP request to domain
        LoanApplication domain = LoanSoapMapper.toDomain(request);
        
        // Execute use case (same as REST!)
        LoanApplication result = loanUseCase.applyForLoan(domain);
        
        // Map domain to SOAP response
        return LoanSoapMapper.toSoap(result);
    }
}
