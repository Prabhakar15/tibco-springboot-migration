package com.example.tibco_migration.endpoint;

import com.example.tibco_migration.dto.*;
import com.example.tibco_migration.service.LoanApplicationService;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

@Endpoint
public class LoanApplicationEndpoint {

    private static final String NAMESPACE_URI = "http://example.com/tibco_migration/loan";

    private final LoanApplicationService service;

    public LoanApplicationEndpoint(LoanApplicationService service) {
        this.service = service;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "LoanApplicationRequest")
    @ResponsePayload
    public LoanApplicationResponse applyForLoan(@RequestPayload LoanApplicationRequest request) {
        return service.applyForLoan(request);
    }
}
