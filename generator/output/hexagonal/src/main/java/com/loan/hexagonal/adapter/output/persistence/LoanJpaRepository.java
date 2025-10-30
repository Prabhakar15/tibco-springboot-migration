package com.loan.hexagonal.adapter.output.persistence;

import com.loan.hexagonal.adapter.output.persistence.entity.LoanEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LoanJpaRepository extends JpaRepository<LoanEntity, String> {
}
