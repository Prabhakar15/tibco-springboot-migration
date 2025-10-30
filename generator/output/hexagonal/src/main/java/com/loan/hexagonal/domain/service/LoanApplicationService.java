package com.loan.hexagonal.domain.service;

import com.loan.hexagonal.domain.model.LoanApplication;
import com.loan.hexagonal.domain.model.CreditScore;
import com.loan.hexagonal.domain.port.input.LoanApplicationUseCase;
import com.loan.hexagonal.domain.port.output.LoanRepository;
import com.loan.hexagonal.domain.port.output.CreditScoreGateway;
import com.loan.hexagonal.domain.port.output.NotificationGateway;

import java.util.UUID;

/**
 * Core business logic for loan application processing.
 * Implements use case by orchestrating domain model and output ports.
 * 
 * NOTE: This is a PURE domain service with NO framework dependencies.
 * Spring configuration happens in the adapter layer (AdapterConfig).
 */
public class LoanApplicationService implements LoanApplicationUseCase {
    
    private final LoanRepository loanRepository;
    private final CreditScoreGateway creditScoreGateway;
    private final NotificationGateway notificationGateway;
    
    public LoanApplicationService(
            LoanRepository loanRepository,
            CreditScoreGateway creditScoreGateway,
            NotificationGateway notificationGateway) {
        this.loanRepository = loanRepository;
        this.creditScoreGateway = creditScoreGateway;
        this.notificationGateway = notificationGateway;
    }
    
    @Override
    public LoanApplication applyForLoan(LoanApplication application) {
        // Generate ID
        application.setId(UUID.randomUUID().toString());
        
        // Check credit score via gateway
        CreditScore score = creditScoreGateway.checkCredit(application.getApplicant());
        application.setCreditScore(score);
        
        // Business rule: approve if score >= 600
        if (score.getScore() >= 600) {
            application.approve();
        } else {
            application.reject("Credit score below minimum threshold");
        }
        
        // Save via repository
        LoanApplication saved = loanRepository.save(application);
        
        // Send notification
        notificationGateway.sendApplicationNotification(saved);
        
        return saved;
    }
    
    @Override
    public LoanApplication getLoanById(String loanId) {
        return loanRepository.findById(loanId)
                .orElseThrow(() -> new IllegalArgumentException("Loan not found: " + loanId));
    }
}
