package com.loan.hexagonal.domain.port.output;

import com.loan.hexagonal.domain.model.ApplicantInfo;
import com.loan.hexagonal.domain.model.CreditScore;

/**
 * Output port for credit score checking.
 * HTTP client adapter will implement this.
 */
public interface CreditScoreGateway {
    CreditScore checkCredit(ApplicantInfo applicant);
}
