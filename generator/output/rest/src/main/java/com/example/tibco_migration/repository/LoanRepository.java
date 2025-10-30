package com.example.tibco_migration.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.tibco_migration.entity.LoanEntity;

@Repository
public interface LoanRepository extends JpaRepository<LoanEntity, Long> {
    LoanEntity findByLoanId(String loanId);
    LoanEntity findByCustomerId(String customerId);
}