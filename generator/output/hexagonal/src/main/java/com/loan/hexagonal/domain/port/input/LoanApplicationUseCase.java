package com.loan.hexagonal.domain.port.input;

import com.loan.hexagonal.domain.model.LoanApplication;

/**
 * Input port for loan application use cases.
 * This is the interface that adapters (REST, SOAP) will call.
 */
public interface LoanApplicationUseCase {
    
    /**
     * Apply for a new loan.
     * @param application The loan application details
     * @return The processed loan application with ID and credit score
     */
    LoanApplication applyForLoan(LoanApplication application);
    
    /**
     * Retrieve a loan application by ID.
     * @param loanId The loan ID
     * @return The loan application if found
     */
    LoanApplication getLoanById(String loanId);
}
