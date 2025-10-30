package com.loan.hexagonal.domain.port.output;

import com.loan.hexagonal.domain.model.LoanApplication;
import java.util.Optional;

/**
 * Output port for loan persistence.
 * Infrastructure adapter will implement this.
 */
public interface LoanRepository {
    LoanApplication save(LoanApplication loan);
    Optional<LoanApplication> findById(String id);
}
