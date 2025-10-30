package com.loan.hexagonal.adapter.output.http;

import com.loan.hexagonal.domain.model.ApplicantInfo;
import com.loan.hexagonal.domain.model.CreditScore;
import com.loan.hexagonal.domain.port.output.CreditScoreGateway;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

/**
 * HTTP adapter for credit score checking.
 * Calls external credit score service.
 */
@Component
public class CreditScoreHttpAdapter implements CreditScoreGateway {
    
    private final WebClient webClient;
    
    public CreditScoreHttpAdapter(
            @Value("${creditscore.service.url:http://localhost:8082/creditscore}") String baseUrl) {
        this.webClient = WebClient.builder()
                .baseUrl(baseUrl)
                .build();
    }
    
    @Override
    public CreditScore checkCredit(ApplicantInfo applicant) {
        // Call external service (simplified)
        try {
            Integer score = webClient.post()
                    .uri("/check")
                    .bodyValue(applicant)
                    .retrieve()
                    .bodyToMono(Integer.class)
                    .block();
            
            return new CreditScore(score != null ? score : 650);
        } catch (Exception e) {
            // Fallback score if service unavailable
            return new CreditScore(650);
        }
    }
}
