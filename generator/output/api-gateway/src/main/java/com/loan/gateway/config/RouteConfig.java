package com.loan.gateway.config;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Route Configuration - Defines all routes for backend services.
 * 
 * Route Patterns:
 * - /api/{service}/** -> REST services (layered or hexagonal)
 * - /ws/{service}/** -> SOAP services (layered or hexagonal)
 * 
 * Features per route:
 * - Path-based routing with prefix stripping
 * - Circuit breaker with fallback
 * - Automatic retry (3 attempts)
 * - Request header tracking
 */
@Configuration
public class RouteConfig {

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
                .route("loanapplicationprocess_hexagonal_route_rest", r -> r
                    .path("/api/loanapplicationprocess/**")
                    .filters(f -> f
                        .stripPrefix(1)
                        .addRequestHeader("X-Gateway-Route", "loanapplicationprocess_hexagonal_route_rest")
                        .circuitBreaker(c -> c
                            .setName("loanapplicationprocess_cb")
                            .setFallbackUri("forward:/fallback/loanapplicationprocess"))
                        .retry(config -> config.setRetries(3)))
                    .uri("http://localhost:8081"))
                .route("loanapplicationprocess_hexagonal_route_soap", r -> r
                    .path("/ws/loanapplicationprocess/**")
                    .filters(f -> f
                        .stripPrefix(1)
                        .addRequestHeader("X-Gateway-Route", "loanapplicationprocess_hexagonal_route_soap")
                        .circuitBreaker(c -> c
                            .setName("loanapplicationprocess_soap_cb")
                            .setFallbackUri("forward:/fallback/loanapplicationprocess")))
                    .uri("http://localhost:8081"))
                .build();
    }
}
