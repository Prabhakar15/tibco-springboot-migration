package com.loan.hexagonal.config;

import com.loan.hexagonal.domain.service.LoanApplicationService;
import com.loan.hexagonal.domain.port.input.LoanApplicationUseCase;
import com.loan.hexagonal.domain.port.output.LoanRepository;
import com.loan.hexagonal.domain.port.output.CreditScoreGateway;
import com.loan.hexagonal.domain.port.output.NotificationGateway;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * Configuration for hexagonal architecture.
 * This is where we wire the domain service with adapter implementations.
 * 
 * The domain service is pure Java - this config adds Spring framework support.
 */
@Configuration
@EnableJpaRepositories(basePackages = "{pkg}.adapter.output.persistence")
@EnableTransactionManagement
public class AdapterConfig {
    
    /**
     * Create the domain service bean.
     * Wire it with output port implementations (adapters).
     * 
     * @param loanRepository JPA persistence adapter
     * @param creditScoreGateway HTTP gateway adapter
     * @param notificationGateway JMS messaging adapter
     * @return The use case implementation
     */
    @Bean
    public LoanApplicationUseCase loanApplicationUseCase(
            LoanRepository loanRepository,
            CreditScoreGateway creditScoreGateway,
            NotificationGateway notificationGateway) {
        return new LoanApplicationService(
            loanRepository,
            creditScoreGateway,
            notificationGateway
        );
    }
}
