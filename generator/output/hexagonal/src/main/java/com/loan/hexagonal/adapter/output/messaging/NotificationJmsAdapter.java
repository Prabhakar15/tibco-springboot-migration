package com.loan.hexagonal.adapter.output.messaging;

import com.loan.hexagonal.domain.model.LoanApplication;
import com.loan.hexagonal.domain.port.output.NotificationGateway;

import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Component;

/**
 * JMS adapter for sending notifications.
 */
@Component
public class NotificationJmsAdapter implements NotificationGateway {
    
    private final JmsTemplate jmsTemplate;
    
    public NotificationJmsAdapter(JmsTemplate jmsTemplate) {
        this.jmsTemplate = jmsTemplate;
    }
    
    @Override
    public void sendApplicationNotification(LoanApplication loan) {
        String message = String.format(
            "Loan Application %s for %s - Status: %s",
            loan.getId(),
            loan.getApplicant().getFullName(),
            loan.getStatus()
        );
        
        jmsTemplate.convertAndSend("loan.notifications", message);
    }
}
