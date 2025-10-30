package com.loan.hexagonal.adapter.input.rest;

import com.loan.hexagonal.domain.port.input.LoanApplicationUseCase;
import com.loan.hexagonal.domain.model.LoanApplication;
import com.loan.hexagonal.adapter.input.rest.dto.LoanRequestDto;
import com.loan.hexagonal.adapter.input.rest.dto.LoanResponseDto;
import com.loan.hexagonal.adapter.input.rest.mapper.LoanDtoMapper;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

/**
 * REST adapter for loan application use case.
 */
@RestController
@RequestMapping("/api/loans")
public class LoanRestController {
    
    private final LoanApplicationUseCase loanUseCase;
    
    public LoanRestController(LoanApplicationUseCase loanUseCase) {
        this.loanUseCase = loanUseCase;
    }
    
    @PostMapping("/apply")
    public ResponseEntity<LoanResponseDto> applyForLoan(@Valid @RequestBody LoanRequestDto dto) {
        // Map DTO to domain
        LoanApplication domain = LoanDtoMapper.toDomain(dto);
        
        // Execute use case
        LoanApplication result = loanUseCase.applyForLoan(domain);
        
        // Map domain to DTO
        LoanResponseDto response = LoanDtoMapper.toDto(result);
        
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/{loanId}")
    public ResponseEntity<LoanResponseDto> getLoan(@PathVariable String loanId) {
        LoanApplication loan = loanUseCase.getLoanById(loanId);
        return ResponseEntity.ok(LoanDtoMapper.toDto(loan));
    }
}
