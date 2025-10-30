package com.loan.gateway.config;

import org.springframework.cloud.gateway.filter.ratelimit.KeyResolver;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import reactor.core.publisher.Mono;

/**
 * Gateway Configuration - Central configuration for API Gateway behavior.
 */
@Configuration
public class GatewayConfig {

    /**
     * Key resolver for rate limiting based on IP address.
     * Can be customized to use user ID, API key, etc.
     */
    @Bean
    public KeyResolver ipKeyResolver() {
        return exchange -> Mono.just(
            exchange.getRequest()
                .getRemoteAddress()
                .getAddress()
                .getHostAddress()
        );
    }
    
    /**
     * Key resolver for rate limiting based on user ID from header.
     * Useful for authenticated requests.
     */
    @Bean
    public KeyResolver userKeyResolver() {
        return exchange -> Mono.justOrEmpty(
            exchange.getRequest()
                .getHeaders()
                .getFirst("X-User-Id")
        ).defaultIfEmpty("anonymous");
    }
}
