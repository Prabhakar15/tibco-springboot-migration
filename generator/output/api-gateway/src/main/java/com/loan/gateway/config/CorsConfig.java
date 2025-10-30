package com.loan.gateway.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.reactive.CorsWebFilter;
import org.springframework.web.cors.reactive.UrlBasedCorsConfigurationSource;

import java.util.Arrays;
import java.util.List;

/**
 * CORS Configuration - Enables cross-origin requests.
 * 
 * Configured to allow:
 * - All origins (customize for production)
 * - Common HTTP methods
 * - Custom headers
 * - Credentials
 */
@Configuration
public class CorsConfig {

    @Bean
    public CorsWebFilter corsWebFilter() {
        CorsConfiguration corsConfig = new CorsConfiguration();
        
        // Allow all origins (customize for production)
        corsConfig.setAllowedOriginPatterns(List.of("*"));
        
        // Allow common HTTP methods
        corsConfig.setAllowedMethods(Arrays.asList(
            "GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"
        ));
        
        // Allow common headers
        corsConfig.setAllowedHeaders(Arrays.asList(
            "Authorization", "Content-Type", "X-User-Id", 
            "X-Request-Id", "X-Correlation-Id"
        ));
        
        // Expose custom headers to client
        corsConfig.setExposedHeaders(Arrays.asList(
            "X-Total-Count", "X-Page-Number", "X-Page-Size"
        ));
        
        // Allow credentials
        corsConfig.setAllowCredentials(true);
        
        // Cache preflight response for 1 hour
        corsConfig.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", corsConfig);
        
        return new CorsWebFilter(source);
    }
}
