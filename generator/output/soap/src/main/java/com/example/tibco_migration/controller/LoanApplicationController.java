package com.example.tibco_migration.controller;

import com.example.tibco_migration.dto.LoanApplicationRequest;
import com.example.tibco_migration.dto.LoanApplicationResponse;
import com.example.tibco_migration.service.LoanApplicationService;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/loan")
public class LoanApplicationController {

    private final LoanApplicationService service;

    public LoanApplicationController(LoanApplicationService service) {
        this.service = service;
    }

    @PostMapping("/apply")
    public ResponseEntity<LoanApplicationResponse> apply(@Valid @RequestBody LoanApplicationRequest request) {
        LoanApplicationResponse resp = service.applyForLoan(request);
        return ResponseEntity.ok(resp);
    }
}
