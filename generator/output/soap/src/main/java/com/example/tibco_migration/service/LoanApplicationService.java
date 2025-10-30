package com.example.tibco_migration.service;

import com.example.tibco_migration.dto.*;
import com.example.tibco_migration.entity.LoanEntity;
import com.example.tibco_migration.repository.LoanRepository;

import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.LocalDateTime;
import java.util.UUID;

@Service
public class LoanApplicationService {

    private final WebClient webClient;
    private final LoanRepository repo;
    private final JmsTemplate jmsTemplate;

    public LoanApplicationService(WebClient webClient, LoanRepository repo, JmsTemplate jmsTemplate) {
        this.webClient = webClient;
        this.repo = repo;
        this.jmsTemplate = jmsTemplate;
    }

    public LoanApplicationResponse applyForLoan(LoanApplicationRequest req) {
        // Create entity and map request data
        LoanEntity loan = new LoanEntity();
        loan.setLoanId(UUID.randomUUID().toString());
        loan.setCustomerId(req.getCustomerID());
        loan.setApplicantName(req.getApplicantName());
        loan.setLoanAmount(req.getLoanAmount());
        loan.setLoanType(req.getLoanType());
        loan.setLoanTermMonths(req.getLoanTermMonths());
        loan.setContactEmail(req.getContactEmail());
        loan.setApplicationDate(LocalDateTime.now());
        loan.setStatus("PENDING");
        
        // Save to database
        loan = repo.save(loan);

        // Call credit score service
        CreditScoreResponse creditScore = webClient.post()
            .uri("/check")
            .bodyValue(new CreditScoreRequest(loan.getCustomerId(), loan.getApplicantName()))
            .retrieve()
            .bodyToMono(CreditScoreResponse.class)
            .block();

        // Process score and update loan status
        String status;
        String message;
        if (creditScore.getScore() > 650) {
            status = "APPROVED";
            message = "Loan application approved";
            loan.setApprovedAmount(loan.getLoanAmount());
        } else {
            status = "REJECTED";
            message = "Credit score below threshold";
            loan.setRejectionReason(message);
        }
        
        loan.setStatus(status);
        repo.save(loan);

        // Send status via JMS
        jmsTemplate.convertAndSend("LoanStatusQueue", loan.getLoanId() + ":" + status);

        // Prepare response
        LoanApplicationResponse response = new LoanApplicationResponse();
        response.setLoanID(loan.getLoanId());
        response.setStatus(status);
        response.setMessage(message);
        if ("APPROVED".equals(status)) {
            response.setApprovedAmount(loan.getApprovedAmount());
        } else {
            response.setRejectionReason(loan.getRejectionReason());
        }
        
        return response;
    }
}
