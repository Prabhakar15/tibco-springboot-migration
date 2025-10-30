package com.loan.hexagonal.adapter.output.persistence;

import com.loan.hexagonal.domain.model.LoanApplication;
import com.loan.hexagonal.domain.port.output.LoanRepository;
import com.loan.hexagonal.adapter.output.persistence.entity.LoanEntity;

import org.springframework.stereotype.Component;
import java.util.Optional;

/**
 * JPA adapter implementing domain repository port.
 */
@Component
public class LoanRepositoryAdapter implements LoanRepository {
    
    private final LoanJpaRepository jpaRepository;
    
    public LoanRepositoryAdapter(LoanJpaRepository jpaRepository) {
        this.jpaRepository = jpaRepository;
    }
    
    @Override
    public LoanApplication save(LoanApplication loan) {
        LoanEntity entity = LoanEntityMapper.toEntity(loan);
        LoanEntity saved = jpaRepository.save(entity);
        return LoanEntityMapper.toDomain(saved);
    }
    
    @Override
    public Optional<LoanApplication> findById(String id) {
        return jpaRepository.findById(id)
                .map(LoanEntityMapper::toDomain);
    }
}
