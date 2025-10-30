package com.loan.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;

/**
 * API Gateway Application - Single entry point for all microservices.
 * 
 * This gateway routes traffic to:
 * - REST services (layered architecture)
 * - SOAP services (layered architecture)
 * - Hexagonal architecture services (REST/SOAP/Combined)
 * 
 * Features:
 * - Path-based routing
 * - CORS configuration
 * - Rate limiting
 * - Circuit breaker integration
 * - Request/response filtering
 * - Load balancing
 */
@SpringBootApplication
public class ApiGatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(ApiGatewayApplication.class, args);
    }
}
