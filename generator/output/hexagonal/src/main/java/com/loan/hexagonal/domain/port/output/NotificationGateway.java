package com.loan.hexagonal.domain.port.output;

import com.loan.hexagonal.domain.model.LoanApplication;

/**
 * Output port for sending notifications.
 * JMS adapter will implement this.
 */
public interface NotificationGateway {
    void sendApplicationNotification(LoanApplication loan);
}
